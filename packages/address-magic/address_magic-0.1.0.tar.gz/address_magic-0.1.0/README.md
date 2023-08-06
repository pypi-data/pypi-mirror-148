
# Table of Contents

# Address magic

Address magic is a wraper around [postal](https://github.com/openvenues/pypostal).

example:

    from address_magic import Address
    address = Address("The Book Club 100-106 Leonard St, Shoreditch, London, Greater London, EC2A 4RH, United Kingdom")
    print(address.road)
    print(address.country)
    print(address.postcode)

