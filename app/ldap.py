from ldap3 import Server, Connection, ALL

def fetch_ldap_user_data(user_uid):
    """
    Fetch LDAP user data for a given UID.

    Args:
        user_uid (str): The UID of the user to search for.

    Returns:
        dict: A dictionary containing user details or None if no data is found.
    """
    try:
        # LDAP server configuration
        server = Server('ldap.iitb.ac.in', get_info=ALL)
        conn = Connection(server)

        # Bind to the LDAP server
        if not conn.bind():
            print("Failed to bind to the server.")
            return None

        # Perform the LDAP search
        search_base = 'ou=People,dc=iitb,dc=ac,dc=in'
        # search_filter = f'(&(employeetype=*)(uid={user_uid}))'
        search_filter = f'(|(&(employeetype=*)(uid={user_uid}))(&(employeetype=*)(employeeNumber={user_uid})))'
        search_attributes = ['gecos', 'mail', 'uidnumber', 'uid', 'departmentnumber','employeeNumber']

        if conn.search(search_base, search_filter, attributes=search_attributes):
            # Extract the first entry (if any)
            if conn.entries:
                entry = conn.entries[0]
                return {
                    'gecos': entry.gecos.value if 'gecos' in entry else None,
                    'mail': entry.mail.value if 'mail' in entry else None,
                    'uidnumber': entry.uidnumber.value if 'uidnumber' in entry else None,
                    'uid': entry.uid.value if 'uid' in entry else None,
                    'departmentnumber': entry.departmentnumber.value if 'departmentnumber' in entry else None,
                    'employeeNumber': entry.employeeNumber.value if 'employeeNumber' in entry else None,
                }
        else:
            print(f"No entries found for UID: {user_uid}")
            return None
    except Exception as e:
        print(f"Error occurred: {e}")
        return None
    finally:
        conn.unbind()
#################################################################
# from ldap3 import Server, Connection, ALL

# def fetch_ldap_user_data(user_uid):
#     """
#     Fetch LDAP user data for a given UID.

#     Args:
#         user_uid (str): The UID of the user to search for.

#     Returns:
#         dict: A dictionary containing user details or None if no data is found.
#     """
#     try:
#         # LDAP server configuration
#         server = Server('ldap.iitb.ac.in', get_info=ALL)
#         conn = Connection(server)

#         # Bind to the LDAP server
#         if not conn.bind():
#             print("Failed to bind to the server.")
#             return None

#         # Perform the LDAP search
#         search_base = 'ou=People,dc=iitb,dc=ac,dc=in'
#         # search_filter = f'(&(employeetype=*)(uid={user_uid}))'
#         search_filter = f'(|(&(employeetype=*)(uid={user_uid}))(&(employeetype=*)(employeeNumber={user_uid})))'
#         search_attributes = ['gecos', 'mail', 'uidnumber', 'uid', 'departmentnumber','employeeNumber']

#         if conn.search(search_base, search_filter, attributes=search_attributes):
#             # Extract the first entry (if any)
#             if conn.entries:
#                 entry = conn.entries[0]
#                 return {
#                     'gecos': entry.gecos.value if 'gecos' in entry else None,
#                     'mail': entry.mail.value if 'mail' in entry else None,
#                     'uidnumber': entry.uidnumber.value if 'uidnumber' in entry else None,
#                     'uid': entry.uid.value if 'uid' in entry else None,
#                     'departmentnumber': entry.departmentnumber.value if 'departmentnumber' in entry else None,
#                     'employeeNumber': entry.employeeNumber.value if 'employeeNumber' in entry else None,
#                 }
#                 print(gcos)
#         else:
#             print(f"No entries found for UID: {user_uid}")
#             return None
#     except Exception as e:
#         print(f"Error occurred: {e}")
#         return None
#     finally:
#         conn.unbind()
# fetch_ldap_user_data('30006141')  # Example usage







###################################################################################################



# from ldap3 import Server, Connection, ALL

# def fetch_ldap_user_data(user_uid):
#     conn = None
#     try:
#         server = Server('ldap.iitb.ac.in', get_info=ALL)
#         conn = Connection(server)

#         if not conn.bind():
#             print("❌ Failed to bind to LDAP server")
#             return None

#         search_base = 'ou=People,dc=iitb,dc=ac,dc=in'
#         search_filter = f'(|(&(employeetype=*)(uid={user_uid}))(&(employeetype=*)(employeeNumber={user_uid})))'
#         search_attributes = ['gecos', 'mail', 'uidnumber', 'uid', 'departmentnumber', 'employeeNumber']

#         conn.search(search_base, search_filter, attributes=search_attributes)

#         if conn.entries:
#             entry = conn.entries[0]

#             result = {
#                 'gecos': entry.gecos.value if 'gecos' in entry else None,
#                 'mail': entry.mail.value if 'mail' in entry else None,
#                 'uidnumber': entry.uidnumber.value if 'uidnumber' in entry else None,
#                 'uid': entry.uid.value if 'uid' in entry else None,
#                 'departmentnumber': entry.departmentnumber.value if 'departmentnumber' in entry else None,
#                 'employeeNumber': entry.employeeNumber.value if 'employeeNumber' in entry else None,
#             }

#             return result

#         else:
#             print(f"⚠️ No entries found for UID: {user_uid}")
#             return None

#     except Exception as e:
#         print(f"❌ Error occurred: {e}")
#         return None

#     finally:
#         if conn:
#             conn.unbind()


# # 🔥 TEST HERE
# if __name__ == "__main__":
#     data = fetch_ldap_user_data('30006141')

#     print("\n===== LDAP RESULT =====")
#     if data:
#         for key, value in data.items():
#             print(f"{key}: {value}")
#     else:
#         print("No data found")



########################################################################
# from ldap3 import Server, Connection, ALL

# def fetch_ldap_user_data(user_uid):
#     try:
#         server = Server('ldap.iitb.ac.in', get_info=ALL)
#         conn = Connection(server)

#         if not conn.bind():
#             print("❌ Failed to bind to LDAP")
#             return {}

#         search_base = 'ou=People,dc=iitb,dc=ac,dc=in'

#         search_filter = f'(|(&(employeetype=*)(uid={user_uid}))(&(employeetype=*)(employeeNumber={user_uid})))'

#         # 🔥 FIX: correct attribute name (case-sensitive)
#         search_attributes = [
#             'gecos',
#             'mail',
#             'uidnumber',
#             'uid',
#             'departmentNumber',   # ✅ FIXED
#             'employeeNumber'
#         ]

#         if conn.search(search_base, search_filter, attributes=search_attributes):
#             if conn.entries:
#                 entry = conn.entries[0]

#                 data = {
#                     'gecos': entry.gecos.value if entry.gecos else '',
#                     'mail': entry.mail.value if entry.mail else '',
#                     'uidnumber': entry.uidnumber.value if entry.uidnumber else '',
#                     'uid': entry.uid.value if entry.uid else '',
#                     'departmentnumber': entry.departmentNumber.value if entry.departmentNumber else '',  # ✅ FIXED
#                     'employeeNumber': entry.employeeNumber.value if entry.employeeNumber else '',
#                 }

#                 print("✅ LDAP DATA:", data)
#                 return data

#         print(f"❌ No entries found for UID: {user_uid}")
#         return {}

#     except Exception as e:
#         print(f"❌ LDAP ERROR: {e}")
#         return {}

#     finally:
#         conn.unbind()