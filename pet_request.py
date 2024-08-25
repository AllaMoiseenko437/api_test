import pytest
import requests
import jsonschema
from jsonschema import validate

base_url = "https://petstore.swagger.io/v2"

@pytest.mark.parametrize("pet_id, pet_name, pet_status, updated_name, updated_status", [
    (14567, "python", "available", "python_updated", "available"),
    (14568, "dog", "available", "dog_updated", "available"),
    (78909, "cat", "pending", "cat_updated", "available")
])
def test_pet_poperation(pet_id, pet_name, pet_status, updated_name, updated_status):
    # Create pet
    data = {
        "id": pet_id,
        "category": {
            "id": 9,
            "name": "python"
        },
        "name": "python",
        "photoUrls": [
            "string"
        ],
        "tags": [
            {
                "id": 10,
                "name": pet_name
            }
        ],
        "status": pet_status
    }

    create_pet = requests.post(f'{base_url}/pet', json=data)
    print("Create pet response: " + create_pet.text)
    assert create_pet.status_code == 200
    print(create_pet.headers)
    assert create_pet.headers['Content-Type'] == 'application/json'

    # Update pet
    update_data = {
        "id": pet_id,
        "category": {
            "id": 9,
            "name": "python_change"
        },
        "name": updated_name,
        "photoUrls": [
            "string"
        ],
        "tags": [
            {
                "id": 10,
                "name": updated_name
            }
        ],
        "status": updated_status
    }

    update_pet = requests.put(f'{base_url}/pet', json=update_data)
    print("Update pet response: " + update_pet.text)
    assert update_pet.status_code == 200
    print(update_pet.headers)
    assert update_pet.headers['Content-Type'] == 'application/json'

    # Get pet
    get_pet = requests.get(f'{base_url}/pet/{pet_id}')
    print("Get pet response: " + get_pet.text)
    assert get_pet.status_code == 200
    print(get_pet.headers)
    assert get_pet.headers['Content-Type'] == 'application/json'
    pet_info = get_pet.json()
    assert pet_info['id'] == pet_id
    assert pet_info['status'] == updated_status
    assert pet_info['name'] == updated_name

    schema = {
        "type": "object",
        "properties": {
            "id": {"type": "integer"},
            "name": {"type": "string"},
            "photoUrls": {"type": "array", "items": {"type": "string"}},
            "tags": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer"},
                        "name": {"type": "string"}
                    },
                    "required": ["id", "name"]
                }
            },
            "status": {"type": "string"}
        },
        "required": ["id", "name", "photoUrls", "tags", "status"],
    }

    try:
        validate(instance=pet_info, schema=schema)
        print("JSON Schema validation success.")
    except jsonschema.exceptions.ValidationError as e:
        print("Erorr validation JSON Schema: ")
        print(e)
        raise e

    # Delete pet
    delete_pet = requests.delete(f'{base_url}/pet/{pet_id}')
    print("Delete pet response: " + delete_pet.text)
    assert delete_pet.status_code == 200
    print(delete_pet.headers)
    assert delete_pet.headers['Content-Type'] == 'application/json'