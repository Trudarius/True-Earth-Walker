# Login Simulator - Day 1 Project

correct_password = "blue42"
attempts = 0
max_attempts = 3

while attempts < max_attempts:
    user_input = input("Enter the password: ")
    
    if user_input != correct_password:
        attempts = attempts + 1
    
    if user_input == "password" or user_input == "1234":
        print("Hacker detected! Logging IP address...")
        attempts = max_attempts
        print("ALERT: Malicious activity detected. Locking system.")
        
    elif user_input == correct_password:
        print("Access Granted.")
        break
        
    else:
        print("Access Denied.")
        if attempts >= max_attempts:
            print("ALERT: Too many failed attempts. Locking system for 5 minutes.")
