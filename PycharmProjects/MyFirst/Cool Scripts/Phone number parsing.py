import phonenumbers
from phonenumbers import geocoder, carrier, timezone

raw_number = input("Enter phone number with country code: ").strip()

try:
    number = phonenumbers.parse(raw_number, None)
except phonenumbers.NumberParseException as e:
    print(f"Error parsing number: {e}")
    exit()

print(f"Valid: {phonenumbers.is_valid_number(number)}")
print(f"Possible: {phonenumbers.is_possible_number(number)}")
print(f"Region: {geocoder.description_for_number(number, 'en')}")
print(f"Carrier: {carrier.name_for_number(number, 'en')}")
print(f"Timezones: {timezone.time_zones_for_number(number)}")
print(f"Country Code: +{number.country_code}")
print(f"National Number: {number.national_number}")