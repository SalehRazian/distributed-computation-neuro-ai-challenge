from flask import Flask, request, send_file
from flask_restful import Api, Resource, reqparse
import dill as pickle
import os
from werkzeug.utils import secure_filename
from dask.distributed import Client

# The path to the upload folder "save"
UPLOAD_FOLDER = "save/"

# Initial variables
app = Flask(__name__)
api = Api(app)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# ID variables
requests_counter = 0
id_array = []
id_filename_dict = {}

# Request parser
get_user_id_args = reqparse.RequestParser()
get_user_id_args.add_argument("id", type=str, help="ID ERROR", required=True)


class Compute(Resource):
    """
    This class is responsible for the requests to the base url.
    """
    @staticmethod
    def get():
        """
        GET request - returns a unique ID to the user by utilizing their input ID.
        :return: A unique ID.
        """
        global id_array
        global requests_counter

        try:
            user_id = get_user_id_args.parse_args()["id"] + "id" + str(requests_counter)
        except:
            app.logger.info("This user did not submit an ID.")
            user_id = "unverified_user_id" + str(requests_counter)

        requests_counter += 1
        id_array.append(user_id)

        return {"id": user_id}

    @staticmethod
    def extract_file(name):
        """
        Function - extracts the information from the provided file.
        :param name: Name of the file.
        :return: The extracted information in a variable.
        """
        try:
            file = request.files[name]
            if file:
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

                with open(UPLOAD_FOLDER + filename, "rb") as byte_file:
                    output = pickle.load(byte_file)

                os.remove(app.config["UPLOAD_FOLDER"] + filename)  # The file is redundant at this point
                return output

        except:
            app.logger("This user did not submit: " + name)

        return None  # No information is extracted

    @staticmethod
    def send_file_to_user(user_id, results):
        """
        Function - Pickle the results into a file and then send the file back to the user (client).
        :param user_id: A unique ID.
        :param results: The results of the function in a dictionary.
        :return: A send_file response or -1 in case of failure.
        """
        global id_filename_dict

        filename_results = str(user_id) + "_results.txt"
        try:
            with open(app.config["UPLOAD_FOLDER"] + filename_results, "wb") as binary_file:
                pickle.dump(results, binary_file)

        except Exception as e:
            app.logger.info(e)
            return -1  # Failure

        id_filename_dict[user_id] = filename_results
        return send_file(app.config["UPLOAD_FOLDER"] + filename_results)

    @staticmethod
    def get_results(function, data_input):
        """
        Function - Sends the function with/without input_data to the scheduler for distributed computation and returns
        the results in a dictionary.
        :param function: A given function.
        :param data_input: A given input.
        :return: A dictionary with the results and error status
        """
        try:
            if data_input is None:
                return {"results": client.submit(function).result(), "error": False}

            else:
                return {"results": client.submit(function, data_input).result(), "error": False}

        except:
            try:
                return {"results": client.submit(function, None).result(), "error": False}

            except Exception as e:
                app.logger.info(e)

        return {"results": None, "error": True}  # Failure

    def post(self):
        """
        POST request - Receives the functions and input form the user (client) and returns the results as a file.
        :return: The file containing the pickled results in a dictionary or -1 in case of failure.
        """
        global id_array
        global client

        try:
            user_id = get_user_id_args.parse_args()["id"]
            if user_id in id_array:
                function = self.extract_file("file_function")
                data_input = self.extract_file("file_input")
                return self.send_file_to_user(user_id, self.get_results(function, data_input))

        except Exception as e:
            app.logger.info(e)

        return -1  # Failure

    @staticmethod
    def patch():
        """
        PATCH request - The user (client) informs the server that the file has reached them successfully. The ID
        variables will be modified accordingly.
        :return: A reference to success or failure to execute the modification.
        """
        global id_array
        global id_filename_dict

        try:
            user_id = get_user_id_args.parse_args()["id"]
            if user_id in id_array:
                id_array.remove(user_id)  # Removing ID
                filename = id_filename_dict[user_id]
                os.remove(app.config["UPLOAD_FOLDER"] + filename)  # Deleting results file
                id_filename_dict.pop(user_id)  # Removing filename ID

        except Exception as e:
            app.logger.info(e)
            return -1  # Failure

        return 201  # Success


api.add_resource(Compute, "/")  # Add to the API resources

if __name__ == "__main__":
    client = Client("tcp://127.0.0.1:55062")  # Client connection - Change when necessary
    app.run(host="127.0.0.1", port=5000, debug=False)  # Flask server connection details - Change when necessary
