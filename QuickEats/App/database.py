import os
import json

class Db:
    def log_in(self, email, password):
        with open('data_files/accounts.json', 'r') as f:
            accounts = json.load(f)
        for mail in accounts:
            if email == mail and accounts[mail][1] == password:
                return 1
        return 0

    def regis_ter(self, name, email, password,address):
        with open('data_files/accounts.json', 'r') as f:
            accounts = json.load(f)
        if email in accounts:
            return 0
        else:
            accounts[email] = [name, password,address]
            with open('data_files/accounts.json', 'w') as f:
                json.dump(accounts, f, indent=4)
            return 1

    def get_name(self, email):
        with open('data_files/accounts.json', 'r') as f:
            accounts = json.load(f)
        return accounts[email][0]

    def get_pass(self, email):
        with open('data_files/accounts.json', 'r') as f:
            accounts = json.load(f)
        return accounts[email][1]

    def get_address(self, email):
        with open('data_files/accounts.json', 'r') as f:
            accounts = json.load(f)
        return accounts[email][2]

    def set_name(self, new_name, email):
        with open('data_files/accounts.json', 'r') as f:
            accounts = json.load(f)
        if email in accounts:
            accounts[email][0] = new_name
            with open('data_files/accounts.json', 'w') as f:
                json.dump(accounts, f, indent=4)
            return 1
        return 0

    def set_password(self, new_password, email):
        with open('data_files/accounts.json', 'r') as f:
            accounts = json.load(f)
        if email in accounts:
            accounts[email][1] = new_password
            with open('data_files/accounts.json', 'w') as f:
                json.dump(accounts, f, indent=4)
            return 1
        return 0

    def set_email(self, existing_email, new_email):
        with open('data_files/accounts.json', 'r') as f:
            accounts = json.load(f)
        if existing_email in accounts:
            accounts[new_email] = accounts.pop(existing_email)
            with open('data_files/accounts.json', 'w') as f:
                json.dump(accounts, f, indent=4)
            return 1
        return 0

    def set_address(self, new_address, email):
        with open('data_files/accounts.json', 'r') as f:
            accounts = json.load(f)
        if email in accounts:
            accounts[email][2] = new_address
            with open('data_files/accounts.json', 'w') as f:
                json.dump(accounts, f, indent=4)
            return 1
        return 0

    def delete_acc(self, email, password):
        with open('data_files/accounts.json', 'r') as f:
            accounts = json.load(f)
        with open('data_files/delivery_records.json', 'r') as file1:
            delivery_record = json.load(file1)
        with open('data_files/records.json', 'r') as file2:
            record = json.load(file2)

        if email in accounts:
            if accounts[email][1] == password:
                del accounts[email]
                with open('data_files/accounts.json', 'w') as f:
                    json.dump(accounts, f, indent=4)
                if email in delivery_record:
                    del delivery_record[email]
                    with open('data_files/delivery_records.json', 'w') as file1:
                        json.dump(delivery_record, file1, indent=4)

                with open('data_files/records.json', 'w') as file2:
                    json.dump({}, file2, indent=4)

                return 1
            return 0
        return -1

    def get_menu(self):
        with open('data_files/menu.json', 'r') as f:
            menu = json.load(f)
        return menu

    def update_to_delivery_records(self, email, parcel_data):
        if os.path.exists('data_files/delivery_records.json') and os.path.getsize('data_files/delivery_records.json') > 0:
            try:
                with open('data_files/delivery_records.json', 'r') as f:
                    data = json.load(f)
            except json.JSONDecodeError:
                data = {}
        else:
            data = {}
        if email not in data:
            data[email] = [parcel_data]
        else:
            data[email].append(parcel_data)
        with open('data_files/delivery_records.json', 'w') as f:
            json.dump(data, f, indent=4)


