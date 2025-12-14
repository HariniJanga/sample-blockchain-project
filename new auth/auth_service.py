# auth_service.py (using hashlib instead of bcrypt)
import hashlib
import json
import os
import secrets
from datetime import datetime

class AuthService:
    def __init__(self):
        self.users_file = 'users.json'
        self.users = self.load_users()
        
    def load_users(self):
        """Load users from JSON file"""
        if os.path.exists(self.users_file):
            try:
                with open(self.users_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                print("Warning: Could not load users file, starting with empty user database")
                return {}
        return {}
    
    def save_users(self):
        """Save users to JSON file"""
        try:
            with open(self.users_file, 'w') as f:
                json.dump(self.users, f, indent=2)
        except IOError as e:
            print(f"Error saving users: {e}")
    
    def hash_password(self, password, salt=None):
        """Hash password with salt using SHA-256"""
        if salt is None:
            salt = secrets.token_hex(32)  # Generate random salt
        
        # Combine password and salt
        password_salt = password + salt
        
        # Hash using SHA-256
        hashed = hashlib.sha256(password_salt.encode('utf-8')).hexdigest()
        
        return hashed, salt
    
    def verify_password(self, password, hashed_password, salt):
        """Verify password against hash"""
        test_hash, _ = self.hash_password(password, salt)
        return test_hash == hashed_password
    
    def authenticate_user(self, username, password):
        """Authenticate user with username and password"""
        if not username or not password:
            return {'success': False, 'error': 'Username and password are required'}
        
        if username not in self.users:
            return {'success': False, 'error': 'Invalid username or password'}
        
        user_data = self.users[username]
        stored_hash = user_data['password']
        salt = user_data['salt']
        
        try:
            if self.verify_password(password, stored_hash, salt):
                # Return user data without password
                user_info = user_data.copy()
                del user_info['password']
                del user_info['salt']
                user_info['last_login'] = datetime.now().isoformat()
                
                # Update last login in storage
                self.users[username]['last_login'] = user_info['last_login']
                self.save_users()
                
                return {'success': True, 'user': user_info}
            else:
                return {'success': False, 'error': 'Invalid username or password'}
        except Exception as e:
            print(f"Authentication error: {e}")
            return {'success': False, 'error': 'Authentication failed'}
    
    def register_user(self, username, email, password, company_name):
        """Register a new user"""
        if not all([username, email, password, company_name]):
            return {'success': False, 'error': 'All fields are required'}
        
        if username in self.users:
            return {'success': False, 'error': 'Username already exists'}
        
        if len(password) < 6:
            return {'success': False, 'error': 'Password must be at least 6 characters long'}
        
        # Check if email already exists
        for user_data in self.users.values():
            if user_data.get('email') == email:
                return {'success': False, 'error': 'Email already registered'}
        
        try:
            # Hash the password
            hashed_password, salt = self.hash_password(password)
            
            # Create user data
            user_data = {
                'username': username,
                'email': email,
                'company_name': company_name,
                'password': hashed_password,
                'salt': salt,
                'role': 'manufacturer',
                'created_at': datetime.now().isoformat(),
                'last_login': None,
                'products_registered': 0
            }
            
            # Save user
            self.users[username] = user_data
            self.save_users()
            
            return {'success': True, 'message': 'User registered successfully'}
            
        except Exception as e:
            print(f"Registration error: {e}")
            return {'success': False, 'error': 'Registration failed'}
    
    def update_user_stats(self, username):
        """Update user statistics"""
        if username in self.users:
            self.users[username]['products_registered'] = self.users[username].get('products_registered', 0) + 1
            self.save_users()
    
    def get_user(self, username):
        """Get user information"""
        if username in self.users:
            user_data = self.users[username].copy()
            del user_data['password']  # Never return password
            del user_data['salt']      # Never return salt
            return user_data
        return None
    
    def change_password(self, username, old_password, new_password):
        """Change user password"""
        if username not in self.users:
            return {'success': False, 'error': 'User not found'}
        
        # Verify old password
        auth_result = self.authenticate_user(username, old_password)
        if not auth_result['success']:
            return {'success': False, 'error': 'Current password is incorrect'}
        
        if len(new_password) < 6:
            return {'success': False, 'error': 'New password must be at least 6 characters long'}
        
        try:
            # Hash new password
            hashed_password, salt = self.hash_password(new_password)
            self.users[username]['password'] = hashed_password
            self.users[username]['salt'] = salt
            self.save_users()
            
            return {'success': True, 'message': 'Password changed successfully'}
        except Exception as e:
            print(f"Password change error: {e}")
            return {'success': False, 'error': 'Password change failed'}
    
    def delete_user(self, username):
        """Delete a user"""
        if username in self.users:
            del self.users[username]
            self.save_users()
            return {'success': True, 'message': 'User deleted successfully'}
        return {'success': False, 'error': 'User not found'}
    
    def list_users(self):
        """List all users (without passwords)"""
        users_list = []
        for username, user_data in self.users.items():
            user_info = user_data.copy()
            del user_info['password']
            del user_info['salt']
            users_list.append(user_info)
        return users_list
    
    def create_default_user(self):
        """Create a default admin user for testing"""
        if 'admin' not in self.users:
            result = self.register_user('admin', 'admin@example.com', 'admin123', 'Admin Company')
            if result['success']:
                print("✅ Default admin user created (username: admin, password: admin123)")
            else:
                print(f"❌ Failed to create default user: {result['error']}")

# Create a global instance
auth = AuthService()

# Create default user if no users exist
if not auth.users:
    print("No users found, creating default admin user...")
    auth.create_default_user()

# Test the service
if __name__ == "__main__":
    print("🔐 Authentication Service Test")
    print("-" * 30)
    
    # Test registration
    print("Testing registration...")
    result = auth.register_user("testuser", "test@example.com", "testpass123", "Test Company")
    print(f"Registration result: {result}")
    
    # Test authentication
    print("\nTesting authentication...")
    result = auth.authenticate_user("testuser", "testpass123")
    print(f"Authentication result: {result}")
    
    # Test wrong password
    print("\nTesting wrong password...")
    result = auth.authenticate_user("testuser", "wrongpass")
    print(f"Wrong password result: {result}")
    
    print("\n✅ Authentication service is working!")