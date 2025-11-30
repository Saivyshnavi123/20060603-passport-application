# 🛂 Passport Management System

A web application for managing passport applications with separate dashboards for users and administrators.

---

## ✨ What This App Does

**For Users:**
- Register and login
- Apply for passport
- Check slot availability for appointments
- View application status (Pending/Approved/Rejected)

**For Admins:**
- View all applications
- Approve or reject applications

---

## 🛠️ Built With

- React (JavaScript library for building UI)
- React Router (for page navigation)
- Backend API (already hosted online)

---

## 📦 What You Need First

### 1. Install Node.js

**Download:** https://nodejs.org/

- Download the **LTS version** (recommended)
- Run the installer
- Click "Next" with all default settings
- **Restart your computer** after installation

**Check if installed:**
```cmd
node --version
npm --version
```
You should see version numbers.

---

## 🚀 How to Run This Project

### Step 1: Open Project Folder in Command Prompt

**Easy Method:**
1. Open the project folder in File Explorer (e.g., `D:\Passport Management`)
2. Click on the address bar at top
3. Type `cmd` and press Enter
4. Command Prompt opens! ✅

**Or use this:**
```cmd
d:
cd "Passport Management"
```

---

### Step 2: Install Dependencies

```cmd
npm install
```

**What this does:**
- Downloads all required libraries
- Takes 2-5 minutes
- Creates a `node_modules` folder

**Wait until you see:** `added XXX packages`

---

### Step 3: Start the Application

```cmd
npm start
```

**What happens:**
- Wait 10-30 seconds
- Browser opens automatically at `http://localhost:3000`
- You see the Login page! 🎉

**If browser doesn't open:**
- Open any browser manually
- Go to: `localhost:3000`

---

### Step 4: Use the Application

**User Side:**
1. Click "Register here" to create account
2. Fill username, email, password
3. Login with your credentials
4. Click "Apply for Passport"
5. Fill the form and select appointment date
6. System checks slot availability
7. Submit application
8. View your applications in dashboard

**Admin Side:**
1. Login with admin credentials
2. View all applications
3. Click any application to see details
4. Approve or Reject pending applications

---

### Stop the Application

Press `Ctrl + C` in the command prompt window.

To run again: `npm start`

---

## 📁 Project Structure

```
Passport Management/
├── public/              # Static files
├── src/
│   ├── components/      # Reusable UI components
│   ├── pages/           # Admin & User dashboards
│   ├── routes/          # Route protection
│   ├── services/        # API calls
│   └── App.jsx          # Main app
└── package.json         # Dependencies list
```

---

## 🔧 Common Commands

```cmd
npm install          # Install dependencies (first time)
npm start            # Run the app
Ctrl + C             # Stop the app
npm run build        # Create production build
```

---

## ❗ Common Problems

### "npm is not recognized"
- Node.js not installed
- **Fix:** Install Node.js and restart computer

### Port 3000 already in use
```cmd
netstat -ano | findstr :3000
taskkill /PID <NUMBER> /F
```

### npm install fails
```cmd
npm cache clean --force
rmdir /s /q node_modules
npm install
```

### Blank page after login
- Press F12, check Console for errors
- Clear browser cache (Ctrl + Shift + Delete)
- Check if API is online

### Login not working
- Check internet connection
- Press F12 → Network tab to see API response
- Try registering new account

---

## 📌 Important Info

**Backend API:** `https://two0060603-passport-application.onrender.com`

**Local URL:** `http://localhost:3000`

**Password Requirements:** Minimum 6 characters

**Browser Support:** Chrome, Firefox, Edge, Safari (latest versions)

---

## 📞 Need Help?

1. Check error message in terminal
2. Press F12 in browser → check Console tab
3. Verify Node.js installed: `node --version`
4. Try fresh install (delete node_modules, run npm install)

---

**Created:** November 2025  
**Tech Stack:** React 18 + React Router + REST API
