import requests
import json
import pytest

pet_name = "Tara"  # Pet name which you can add
status_code_ok = 200

class Test():

    @pytest.fixture
    def global_var(self):
        pytest.pet_id_assigned = 0

    def getting_pet_dictionary(self, id):
        '''
        Return the pet dictionary for a given pet id
        '''

        pet_link = 'https://petstore.swagger.io/v2/pet/' + str(id)
        response = requests.get(pet_link)
        pet_dict = json.loads(response.content)
        return pet_dict

    def test_getting_available_pets(self):
        """
        This test checks that it is possible to request AVAILABLE pets to demo pet store through API
        """
        print("\nPerforming test...")

        ###############################################################################################
        # ACTION 1 - Request to API
        ###############################################################################################
        response = requests.get('https://petstore.swagger.io/v2/pet/findByStatus?status=available')

        ###############################################################################################
        # EXPECTATION - API response is 'status_code_ok'
        ###############################################################################################
        assert response.status_code == status_code_ok


    def test_adding_new_available_pet(self):
        """
        This test checks that a new available pet can be added successfully to demo pet store through API
        """
        print("\nPerforming test...")

        ###############################################################################################
        # ACTION 1 - Request to add an available pet
        ###############################################################################################
        print("Adding pet...")
        response = requests.post("https://petstore.swagger.io/v2/pet", json={
            "id": 0,
            "category": {
                "id": 0,
                "name": "string"
            },
            "name": pet_name,
            "photoUrls": [
                "string"
            ],
            "tags": [
                {
                    "id": 0,
                    "name": "string"
                }
            ],
            "status": "available"
        })
        print("Pet has been added as AVAILABLE --> ", response.content)

        ###############################################################################################
        # EXPECTATION 1 - API response is 'status_code_ok'
        ###############################################################################################
        assert response.status_code == status_code_ok

        ###############################################################################################
        # ACTION 2 - Get 'id' that has been assigned
        ###############################################################################################
        pet_dict = json.loads(response.content)
        pytest.pet_id_assigned = pet_dict["id"]
        print("Assigned ID is ", pytest.pet_id_assigned)

        ###############################################################################################
        # EXPECTATION 2 - Status is AVAILABLE
        ###############################################################################################
        assert pet_dict["status"] == 'available'


    def test_updating_status_to_sold(self):
        """
        This test checks that it is possible to change status to SOLD for a given existing pet
        """
        print("\nPerforming test...")

        ###############################################################################################
        # ACTION 1 - Change 'status' to SOLD
        ###############################################################################################
        print("Changing status to SOLD...")
        requests.put("https://petstore.swagger.io/v2/pet/", json={
            "id": pytest.pet_id_assigned,
            "category": {
                "id": 0,
                "name": "string"
            },
            "name": pet_name,
            "photoUrls": [
                "string"
            ],
            "tags": [
                {
                    "id": 0,
                    "name": "string"
                }
            ],
            "status": "sold"
        })

        ###############################################################################################
        # EXPECTATION - Status is SOLD
        ###############################################################################################
        pet_dict = self.getting_pet_dictionary(pytest.pet_id_assigned)
        print("Pet status has been changed to SOLD --> ", pet_dict)
        assert pet_dict["status"] == 'sold'


    def test_deleting_pet(self):
        """
        This test checks the added pet can be deleted from demo pet store through API
        """
        print("\nPerforming test...")

        ###############################################################################################
        # ACTION 1 - Delete pet
        ###############################################################################################
        print("Deleting pet...")
        pet_link = 'https://petstore.swagger.io/v2/pet/' + str(pytest.pet_id_assigned)
        response = requests.delete(pet_link)

        ###############################################################################################
        # EXPECTATION 1 - API response is 'status_code_ok'
        ###############################################################################################
        assert response.status_code == status_code_ok

        ###############################################################################################
        # ACTION 2 - Request
        ###############################################################################################
        print("Requesting deleted pet...")
        pet_dict = self.getting_pet_dictionary(pytest.pet_id_assigned)

        ###############################################################################################
        # EXPECTATION 2 - Pet doesn't exist on database
        ###############################################################################################
        if pet_dict["message"] == 'Pet not found':
            print("Pet ID", pytest.pet_id_assigned, "was deleted successfully --> ", pet_dict)
            assert 1
