from django.shortcuts import render

import pandas as pd
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .models import Document
from .forms import ExcelForm
from .forms import AdvancedSearchExcel
from .models import DataRecord, Receipt
from django.contrib import messages
#from .utils import excel_serial_to_datetime  # Import the conversion function
from datetime import datetime, date as dt_date, timedelta

from .forms import TestForm

#from .util import extract_data_by_column

#receipts_df = pd.read_excel(file_path, sheet_name='Receipts')
#money_collected_df = pd.read_excel(file_path, sheet_name='Money Collected')

def fooddata(request):
  template = loader.get_template('home.html')
  return HttpResponse(template.render())


def read_excel_file(file):
    df = pd.read_excel(file, engine='openpyxl', skiprows=2)
    return df


def excel_serial_to_datetime(serial):
    if isinstance(serial, (int, float)):
        base_date = datetime(1899, 12, 30)
        return base_date + timedelta(days=int(serial))
    raise ValueError("Unsupported date format")


def view_documents(request):
    if request.method == 'POST':
        file_id = request.POST.get('file_id')
        if file_id:
            try:
                document = Document.objects.get(id=file_id)
                document.delete()
                messages.success(request, 'Document deleted successfully.')
            except Document.DoesNotExist:
                messages.error(request, 'Document does not exist.')
            return redirect('view_documents')

    documents = Document.objects.all()
    return render(request, 'view_documents.html', {'documents': documents})


def upload_file(request):
    if request.method == 'POST':
        form = ExcelForm(request.POST, request.FILES)
        if form.is_valid():
            files = request.FILES.getlist('files')  # Get list of uploaded files
            all_data = []  # List to collect data from all files

            for file in files:
                try:
                    # Assuming Document model accepts a file
                    document = Document(file=file)
                    document.save()

                    # Read the Excel file
                    df_dict = pd.read_excel(file, engine='openpyxl', sheet_name=None, skiprows=2)
                    
                    # Process each sheet
                    for sheet_name, df in df_dict.items():
                        # Ensure the 'DATE' column is parsed as datetime
                        if 'DATE' in df.columns:
                            df['DATE'] = pd.to_datetime(df['DATE'], errors='coerce')
                            df['DATE'] = df['DATE'].astype(str)

                        # Append the dataframe to our list of all data
                        all_data.append(df)
                except Exception as e:
                    return render(request, 'upload_file.html', {
                        'form': form,
                        'error': f'Error processing file {file.name}: {e}'
                    })

            # Concatenate all dataframes into one
            if all_data:  # Check if there is any data to concatenate
                full_df = pd.concat(all_data, ignore_index=True)

                # Store the combined dataframe in the session
                request.session['data'] = full_df.to_dict(orient='records')

            # Redirect to view_documents after successful upload
            return redirect('view_documents')
        else:
            return render(request, 'upload_file.html', {
                'form': form,
                'error': 'Form is not valid.'
            })
    else:
        form = ExcelForm()
    
    return render(request, 'upload_file.html', {'form': form})




def data_summary(request):
    form = AdvancedSearchExcel(request.POST or None)
    data = []
    error = None

    specific_date = request.GET.get('specific_date', request.POST.get('specific_date'))
    start_date = request.GET.get('start_date', request.POST.get('start_date'))
    end_date = request.GET.get('end_date', request.POST.get('end_date'))
    lunch_item = request.GET.get('lunch_item', request.POST.get('lunch_item'))

    if request.method == 'POST' and form.is_valid():
        specific_date = form.cleaned_data.get('specific_date')
        start_date = form.cleaned_data.get('start_date')
        end_date = form.cleaned_data.get('end_date')
        lunch_item = form.cleaned_data.get('lunch_item')

    try:
        documents = Document.objects.all()
        all_data = []

        for document in documents:
            file_path = document.file.path
            df_dict = pd.read_excel(file_path, engine='openpyxl', sheet_name=None, skiprows=2)

            for sheet_name, df in df_dict.items():
                if 'DATE' in df.columns:
                    df['DATE'] = pd.to_datetime(df['DATE'], errors='coerce')
                    df = df[df['DATE'].notnull()]
                    all_data.append(df)

        full_df = pd.concat(all_data, ignore_index=True)

        if 'DATE' not in full_df.columns:
            raise KeyError("'DATE' column is missing from the DataFrame.")

        full_df['DATE'] = full_df['DATE'].dt.date

        # Ensure column names are stripped of whitespace
        full_df.columns = full_df.columns.str.strip()
        
        # Add placeholder image
        full_df['Image'] = 'https://via.placeholder.com/30'

        if specific_date:
            query_date = pd.to_datetime(specific_date).date()
            row = full_df[full_df['DATE'] == query_date]
            if row.empty:
                error = f"No data found for date {query_date}."
            else:
                data = row.fillna('').to_dict(orient='records')
        elif start_date and end_date:
            start_date = pd.to_datetime(start_date).date() if start_date else None
            end_date = pd.to_datetime(end_date).date() if end_date else None
            if start_date and end_date and start_date > end_date:
                error = 'Start date cannot be after end date.'
            else:
                rows = full_df[(full_df['DATE'] >= start_date) & (full_df['DATE'] <= end_date)]
                if rows.empty:
                    error = f"No data found between {start_date} and {end_date}."
                else:
                    data = rows.fillna('').to_dict(orient='records')

        elif lunch_item:
            # Make sure the column name matches exactly
            full_df['LUNCH MENU'] = full_df['LUNCH MENU'].fillna('')
            rows = full_df[full_df['LUNCH MENU'].str.contains(lunch_item, case=False, na=False)]
            if rows.empty:
                error = f"No data found for lunch menu item containing '{lunch_item}'."
            else:
                data = rows.fillna('').to_dict(orient='records')
        else:
            error = 'Please provide either a specific date, a date range, or a lunch menu item to search.'

    except ValueError as e:
        error = f'Invalid date format: {e}'
    except KeyError as e:
        error = str(e)

    return render(request, 'data_summary.html', {
        'form': form,
        'data': data,
        'error': error,
        'specific_date': specific_date,
        'start_date': start_date,
        'end_date': end_date,
        'lunch_item': lunch_item,
    })

def receipts(request): {
    
    
}

def upload_receipts(request):
    if request.method == 'POST':
        form = ExcelForm(request.POST, request.FILES)
        if form.is_valid():
            receipts = request.FILES.getlist('receipts')  # Get list of uploaded files
            all_data = []  # List to collect data from all files

            for receipt in receipts:
                try:
                    # Assuming Document model accepts a file
                    document = Document(file=file)
                    document.save()

                    # Read the Excel file
                    df_dict = pd.read_excel(file, engine='openpyxl', sheet_name=None, skiprows=0)
                    
                    # Process each sheet
                    for sheet_name, df in df_dict.items():
                        # Ensure the 'DATE' column is parsed as datetime
                        if 'DATE' in df.columns:
                            df['DATE'] = pd.to_datetime(df['DATE'], errors='coerce')
                            df['DATE'] = df['DATE'].astype(str)

                        # Append the dataframe to our list of all data
                        all_data.append(df)
                except Exception as e:
                    return render(request, 'upload_file.html', {
                        'form': form,
                        'error': f'Error processing file {file.name}: {e}'
                    })

            # Concatenate all dataframes into one
            if all_data:  # Check if there is any data to concatenate
                full_df = pd.concat(all_data, ignore_index=True)

                # Store the combined dataframe in the session
                request.session['data'] = full_df.to_dict(orient='records')

            # Redirect to view_documents after successful upload
            return redirect('view_documents')
        else:
            return render(request, 'upload_file.html', {
                'form': form,
                'error': 'Form is not valid.'
            })
    else:
        form = ExcelForm()
    
    return render(request, 'upload_file.html', {'form': form})    




def test_form(request):
    if request.method == 'POST':
        form = TestForm(request.POST)
        if form.is_valid():
            # Access form data
            test_data = form.cleaned_data['test_field']
            print(f"Received data: {test_data}")  # Log to console for debugging
            # Pass data to the template if needed
            return render(request, 'test_view.html', {'form': form, 'data': test_data})
    else:
        form = TestForm()
    
    return render(request, 'test_view.html', {'form': form})








