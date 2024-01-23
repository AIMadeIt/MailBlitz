import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json
import time
import subprocess
import random
import platform
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Function to check and install missing modules
def check_and_install_modules():
    modules_to_check = ['colorama']

    try:
        import smtplib
    except ImportError:
        print(Fore.RED + "smtplib module not found. Installing..." + Style.RESET_ALL)
        modules_to_check.append('secure-smtplib')

    for module in modules_to_check:
        try:
            __import__(module)
        except ImportError:
            print(Fore.RED + f"{module} module not found. Installing..." + Style.RESET_ALL)
            subprocess.run(['pip', 'install', module])

# Check and install missing modules
check_and_install_modules()

# Function to load user settings from JSON file
def load_settings():
    try:
        with open('settings.json', 'r') as file:
            settings = json.load(file)
    except FileNotFoundError:
        settings = {'email_lists': {}, 'ionos_users': {}, 'timing': 300}
    return settings

# Function to save user settings to JSON file
def save_settings(settings):
    with open('settings.json', 'w') as file:
        json.dump(settings, file, indent=2)

# Function to send email with random subject and message
def send_email(sender_email, sender_password, receiver_email):
    try:
        random_subject = f"Random Subject {random.randint(1, 100)}"
        random_message = f"Random Message {random.randint(1, 100)}"

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = random_subject
        msg.attach(MIMEText(random_message, 'plain'))

        with smtplib.SMTP('smtp.ionos.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
            print(Fore.GREEN + f"Email sent to {receiver_email}" + Style.RESET_ALL)
    except KeyboardInterrupt:
        raise  # Re-raise the KeyboardInterrupt to exit the script
    except Exception as e:
        print(Fore.RED + f"Error sending email to {receiver_email}: {e}" + Style.RESET_ALL)

# Function to make email list
def make_email_list(settings):
    email_list_name = input("Enter a name for the email list: ")
    email_list = []
    while True:
        email = input("Enter an email address (leave blank to finish): ")
        if not email:
            break
        email_list.append(email)

    settings['email_lists'][email_list_name] = email_list
    save_settings(settings)
    print(Fore.GREEN + f"Email list '{email_list_name}' created successfully." + Style.RESET_ALL)

# Function to select email list
def select_email_list(settings):
    print(Fore.CYAN + "Available Email Lists:" + Style.RESET_ALL)
    for name in settings['email_lists']:
        print(name)
    selected_list_name = input("Enter the name of the email list to select: ")
    return settings['email_lists'].get(selected_list_name, [])

# Function to delete email list
def delete_email_list(settings):
    print(Fore.CYAN + "Available Email Lists:" + Style.RESET_ALL)
    for name in settings['email_lists']:
        print(name)
    list_to_delete = input("Enter the name of the email list to delete: ")
    if list_to_delete in settings['email_lists']:
        del settings['email_lists'][list_to_delete]
        save_settings(settings)
        print(Fore.GREEN + f"Email list '{list_to_delete}' deleted successfully." + Style.RESET_ALL)
    else:
        print(Fore.RED + f"Email list '{list_to_delete}' not found." + Style.RESET_ALL)

# Function to add Ionos user
def add_ionos_user(settings):
    ionos_user = input("Enter your Ionos SMTP email address: ")
    ionos_password = input("Enter your Ionos SMTP email password: ")
    settings['ionos_users'][ionos_user] = ionos_password
    save_settings(settings)
    print(Fore.GREEN + "Ionos user added successfully." + Style.RESET_ALL)

# Function to select Ionos user
def select_ionos_user(settings):
    print(Fore.CYAN + "Available Ionos Users:" + Style.RESET_ALL)
    for user in settings['ionos_users']:
        print(user)
    selected_user = input("Enter the Ionos user to select: ")
    return selected_user if selected_user in settings['ionos_users'] else None

# Function to delete Ionos user
def delete_ionos_user(settings):
    print(Fore.CYAN + "Available Ionos Users:" + Style.RESET_ALL)
    for user in settings['ionos_users']:
        print(user)
    user_to_delete = input("Enter the Ionos user to delete: ")
    if user_to_delete in settings['ionos_users']:
        del settings['ionos_users'][user_to_delete]
        save_settings(settings)
        print(Fore.GREEN + f"Ionos user '{user_to_delete}' deleted successfully." + Style.RESET_ALL)
    else:
        print(Fore.RED + f"Ionos user '{user_to_delete}' not found." + Style.RESET_ALL)

# Function to set timing
def set_timing(settings):
    new_timing = int(input("Enter the timing between sent emails (in seconds): "))
    settings['timing'] = new_timing
    save_settings(settings)
    print(Fore.GREEN + "Timing set successfully." + Style.RESET_ALL)

# Function to clear the screen based on the platform
def clear_screen():
    system_platform = platform.system()
    if system_platform == 'Windows':
        subprocess.run(['cls'], shell=True)
    else:
        subprocess.run(['clear'], shell=True)

# Main menu
def main_menu():
    settings = load_settings()
    selected_user = None
    selected_list = None
    total_emails_sent = 0
    while True:
        clear_screen()
        print(Fore.YELLOW + f"Timing between sent emails: {settings['timing']} seconds" + Style.RESET_ALL)
        if selected_user:
            print(Fore.YELLOW + f"Selected Ionos User: {selected_user}" + Style.RESET_ALL)
        if selected_list:
            print(Fore.YELLOW + f"Selected Email List: {selected_list}" + Style.RESET_ALL)
        print(Fore.YELLOW + "Press Q to stop sending emails" + Style.RESET_ALL)
        print(Fore.YELLOW + "\nMain Menu:" + Style.RESET_ALL)
        print("1. Make Email List")
        print("2. Select Email List")
        print("3. Delete Email List")
        print("4. Add Ionos User")
        print("5. Select Ionos User")
        print("6. Delete Ionos User")
        print("7. Set Timing")
        print("8. Start Sending Emails")
        print("9. Quit")

        choice = input("Enter your choice (1-9): ")

        if choice == '1':
            make_email_list(settings)
        elif choice == '2':
            selected_list = select_email_list(settings)
            if selected_list and selected_user:
                total_emails_sent = 0
        elif choice == '3':
            delete_email_list(settings)
        elif choice == '4':
            add_ionos_user(settings)
        elif choice == '5':
            selected_user = select_ionos_user(settings)
        elif choice == '6':
            delete_ionos_user(settings)
        elif choice == '7':
            set_timing(settings)
        elif choice == '8':
            if selected_list and selected_user:
                try:
                    while True:
                        for receiver_email in selected_list:
                            send_email(selected_user, settings['ionos_users'][selected_user], receiver_email)
                            total_emails_sent += 1
                            time.sleep(settings['timing'])
                            clear_screen()  # Clear the screen after each email sent
                            print(Fore.YELLOW + "Press Q to stop sending emails" + Style.RESET_ALL)
                except KeyboardInterrupt:
                    pass  # Ignore KeyboardInterrupt when sending emails is interrupted
                print(Fore.GREEN + f"Total emails sent: {total_emails_sent}" + Style.RESET_ALL)
                input("Press Enter to continue...")
        elif choice == '9':
            print(Fore.RED + "Exiting..." + Style.RESET_ALL)
            break
        else:
            print(Fore.RED + "Invalid choice. Please enter a number between 1 and 9." + Style.RESET_ALL)

if __name__ == "__main__":
    main_menu()
