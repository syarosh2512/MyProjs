from countryinfo import CountryInfo
country = CountryInfo(input("Enter your country: "))
print("Country name is : ", country.name())
print("Capital is : ", country.capital())
print("Currencies is : ", country.currencies())
print("Language is : ", country.languages())
print("Borders are : ", country.borders())
print("Others names : ", country.alt_spellings())

