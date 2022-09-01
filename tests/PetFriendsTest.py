import pytest
import requests
from api import PetFriends
from settings import valid_mail, valid_password, invalid_password, invalid_mail
import os

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_mail, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    _, auth_key = pf.get_api_key(valid_mail, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0

def test_post_add_new_pet_with_valid_data(name='гуляш', animal_type='гусь', age= '2', pet_photo='images/Domestic_Goose.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_mail, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name

def test_successful_delete_self_pet():
    _, auth_key = pf.get_api_key(valid_mail, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, name='котя', animal_type='кот', age='2', pet_photo='images/Domestic_Goose.jpg')
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    assert status == 200
    assert pet_id not in my_pets.values()

def test_successful_update_self_pet_info(name='гуляш', animal_type='гусь', age= '1'):
    _, auth_key = pf.get_api_key(valid_mail, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("There is no my pets")

def test_post_add_new_pet_without_photo(name='шашлык', animal_type='гусёк', age= '3'):
    _, auth_key = pf.get_api_key(valid_mail, valid_password)
    status, result = pf.add_info_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name

def test_post_add_photo(pet_photo='images/Domestic_Goose.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_mail, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) > 0:
        status, result = pf.add_photo_pet(auth_key, my_pets['pets'][0]['id'], pet_photo)
        assert status == 200
        assert 'pet_photo' in result
    else:
        raise Exception("There is no my pets")

def test_get_api_without_pass(email=valid_mail, password=invalid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result

def test_get_api_without_email(email=invalid_mail, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result

def test_get_my_pets_with_valid_key(filter='my_pets'):
    _, auth_key = pf.get_api_key(valid_mail, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0 or len(result['pets']) ==0

def test_get_invalid_filter_with_valid_key(filter='cheloveki'):
    _, auth_key = pf.get_api_key(valid_mail, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status != 200
    assert "Filter value is incorrect" in result

def test_post_new_pet_with_null_data(name='', animal_type='',age='', pet_photo='images/Domestic_Goose.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_mail, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status != 200
    #баг

def test_delete_invalid_pet():
    _, auth_key = pf.get_api_key(valid_mail, valid_password)
    pet_id = '2345678jgd'
    status, result = pf.delete_pet(auth_key, pet_id)
    assert status != 200
    #баг

def test_post_create_pet_with_novalid_key(name="жена", animal_type="Собака", age='38'):
    auth_key = {"key": '3nfjnvcnkldod3okfkdmfnvj4ii3klmkmdkjnfjndjnfdjkndmm'}
    status, result = pf.add_info_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status != 200

def test_get_api_without_email_pass(email=invalid_mail, password=invalid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result







