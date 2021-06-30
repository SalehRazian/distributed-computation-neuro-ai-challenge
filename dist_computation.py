import requests
import random
import string
import dill as pickle
import os


class compute_this:
    """
    This class will decorate a given function and will help us connect to a flask server for distributed computing.
    """

    def __init__(self, function):
        """
        Initialization
        :param function: A given function
        """
        self._function = function

        # The base is the url for connection - Change when necessary
        self._base = "http://127.0.0.1:5000/"

    def __call__(self, x):
        """
        This function gets called when a given function object is ran as a normal function.
        :param x: A given input.
        :return: The output computed locally.
        """
        return self._function(x)

    def __call__(self):
        """
        This function gets called when a given function object is ran as a normal function.
        :return: The output computed locally.
        """
        return self._function()

    @staticmethod
    def random_id():
        """
        Generate a string of 16 random characters.
        :return: A string of random characters - ID
        """
        return "".join(random.choice(string.ascii_letters + string.digits) for _ in range(16))

    @staticmethod
    def generate_file(user_id, pickle_input, name):
        """
        Creates a file that stores the pickled variable.
        :param user_id: The unique ID.
        :param pickle_input: The variable input.
        :param name: The name of the file's suffix.
        :return: The filename of the created file.
        """
        filename = str(user_id) + name
        with open(filename, "wb") as binary_file:
            pickle.dump(pickle_input, binary_file)
        return filename

    def start_connection(self):
        """
        This function starts a connection by getting an ID and creating a file that stores the given function.
        :return: The ID and the filename.
        """
        user_id = requests.get(self._base, {"id": self.random_id()}).json()["id"]
        filename_function = self.generate_file(user_id, self._function, "_function.txt")
        return user_id, filename_function

    def extract_results(self, user_id, results):
        """
        This function extracts the pickled output from the response object "results"
        :param user_id: The unique ID.
        :param results: The response object.
        :return: The output of the function in a dictionary.
        """
        # Saving the response object content in a file.
        filename_results = str(user_id) + "_results.txt"
        file = open(filename_results, "wb")
        file.write(results.content)
        file.close()

        # Extracting the output from the file and deleting the file.
        with open(filename_results, "rb") as file:
            output = pickle.load(file)
        os.remove(filename_results)

        # Informing the server that the file is received and the unique ID is no longer valid.
        requests.patch(self._base, {"id": user_id})

        return output

    def compute(self):
        """
        This function is responsible for the distributive computation (without input values).
        :return: Computed output.
        """
        # Start connection
        user_id, filename_function = self.start_connection()

        # Getting a response from the POST (The results)
        results = requests.post(self._base, {"id": user_id},
                                files={"file_function": (filename_function, open(filename_function, "rb"))})

        # Deleting unwanted files
        os.remove(filename_function)

        # In case there was an error in the server
        if results.content == -1:
            return self._function()

        # Extract the output from the response object (The results)
        output = self.extract_results(user_id, results)

        # In case the output was invalid
        if output["error"]:
            return self._function()

        return output["results"]

    def compute(self, x):
        """
        This function is responsible for the distributive computation (with input values).
        :param x: A given input.
        :return: Computed output.
        """
        # Start connection
        user_id, filename_function = self.start_connection()

        # Generate a file containing the inputs "x"
        filename_input = self.generate_file(user_id, x, "_input.txt")

        # Getting a response from the POST (The results)
        results = requests.post(self._base, {"id": user_id},
                                files={"file_function": (filename_function, open(filename_function, "rb")),
                                       "file_input": (filename_input, open(filename_input, "rb"))})

        # Deleting unwanted files
        os.remove(filename_function)
        os.remove(filename_input)

        # In case there was an error in the server
        if results.content == -1:
            return self._function(x)

        # Extract the output from the response object (The results)
        output = self.extract_results(user_id, results)

        # In case the output was invalid
        if output["error"]:
            return self._function(x)

        return output["results"]
