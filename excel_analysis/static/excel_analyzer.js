const analyzer_container = document.querySelector('.analyzer_container');
const excel_upload_form = document.querySelector('.analyzer_components .excel_upload_form');
const status_message = document.querySelector('.analyzer_components .status_message');
const result_link = document.querySelector('.analyzer_components .result_link');



const save_and_process_excel_file = async () => {
    const fileInput = document.getElementById('excel_file');
    const file = fileInput.files[0];

    if (!file) {
        alert('No file selected');
        return;
    }

    status_message.textContent = 'Processing. . .';

    const formData = new FormData();
    // attach the column name with the file
    formData.append(excel_upload_form.sheet_names.value, file);
    // send data and file to server for processing
    const response = await fetch('http://127.0.0.1:5000/excel_analyzer', {
        method: 'POST',
        body: formData
    });
    // await confirmation response
    const process_response = await response.json();
    if (process_response.message === 'completed') {
        await fetch_excel_file(process_response.filename);
        status_message.textContent = 'Done!\nProceed to Download.';
        // reset form after process is done
        excel_upload_form.reset();
    } else {
        status_message.textContent = process_response.message;
    }
}

// fetch excel file
const fetch_excel_file = async (filename) => {
    const file_response = await fetch('http://127.0.0.1:5000/excel_file');
    const file_data = await file_response.blob();
    
    const url = window.URL.createObjectURL(file_data);

    result_link.setAttribute('href', url);
    result_link.setAttribute('download', filename);
}


// processing form data
const process_form_data = (e) => {
    // to prevent form from refreshing after submitting
    e.preventDefault();
    
    // save user data
    save_and_process_excel_file();
}


// EventListeners
excel_upload_form.addEventListener('submit', process_form_data);