from werkzeug.utils import secure_filename
import os, tempfile
from src.exceptions.operationshandler import system_logger
from main import SimpleDirectoryReader, VectorStoreIndex


allowed_files = ['pdf', 'doc', 'txt', 'pptx', 'csv', 'json']

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_files



def file_checks(files):
    if not files:
        return {
            "details": "No file found",
            "status_code": 400
        }

    for file in files:
        if not file or file.filename == '':
            return {
                "details": "No file found",
                "status_code": 400
            }
        
        if not allowed_file(file.filename):
            print(file.filename)
            return {
                "detail": f"file format not supported. Use any of {allowed_files}",
                "status_code": 400
            }
        
    return {
    "details": "success",
    "status_code": 200
    }

class UploadError(Exception):
    pass


def upload_file(files):

    checks = file_checks(files)
    
    if checks["status_code"] == 200:
        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                for file in files:
                    filename = secure_filename(file.filename)
                    file_path = os.path.join(temp_dir, filename)

                    file_obj = file.read()

                    with open(file_path, "wb") as buffer:
                        buffer.write(file_obj)

                documents = SimpleDirectoryReader(temp_dir).load_data()
                embeddings = VectorStoreIndex.from_documents(documents)

            return {
                "details": "Embeddings generated successfully",
                "status_code": 200
            }

        except Exception:
            message = f"An error occurred during upload"
            system_logger.error(
                message,
                # str(e)
                exc_info=1
            )
            raise UploadError(message)
        
    return checks