# ROBO DIGITAL COMPUTERS --- Service Management System

A complete Django-based **Service Management System** for ROBO DIGITAL
COMPUTERS to manage computer, laptop, printer and other technical
services from service inward to delivery, including customer management,
service ledger, expenses, payments, billing, reports and WhatsApp
notifications.

------------------------------------------------------------------------

## 1. Project Overview

**ROBO DIGITAL COMPUTERS** provides:

-   Computer Sales & Service
-   Laptop Chip Level Service
-   CCTV Camera Installation
-   Printer & UPS Sales & Service
-   Xerox, Color Print & Scan
-   All Type Online Work
-   Tamil & English Typing

This project has two major parts:

### Public Website

A professional company website where customers can:

-   Learn about the company
-   View services
-   View portfolio/work
-   Contact the company
-   Access the Service Management Login

### Private Service Management System

A secure internal application used by authorized staff to:

-   Register incoming devices
-   Manage customers
-   Track service status
-   Record diagnosis and work progress
-   Track expenses
-   Record payments
-   Maintain a complete service ledger
-   Generate bills
-   Send WhatsApp notifications
-   Generate monthly/yearly reports

------------------------------------------------------------------------

# 2. Main Goal

The main goal is to replace manual service records with a centralized
digital system.

The complete business workflow is:

``` text
Customer brings device
        ↓
Create Customer / Find Existing Customer
        ↓
Create Service Inward
        ↓
Generate Service ID
        ↓
Record Device + Complaint + Accessories
        ↓
Automatically record Staff
        ↓
Send WhatsApp Inward Notification
        ↓
Diagnosis
        ↓
Work In Progress
        ↓
Record Parts / Expenses / Work Updates
        ↓
Record Payments
        ↓
Mark Service Completed
        ↓
Generate Bill
        ↓
Send WhatsApp Completion Notification
        ↓
Customer Collects Device
        ↓
Mark Delivered
        ↓
Complete Service Ledger
```

------------------------------------------------------------------------

# 3. Technology Stack

## Backend

-   Python
-   Django 5.2.5
-   Django Authentication
-   Django ORM
-   Django Admin

## Database

-   MySQL

## Frontend

-   HTML5
-   CSS3
-   JavaScript
-   Bootstrap 5
-   Bootstrap Icons

## External Integration

-   WhatsApp Business Platform/API

## Reports

-   CSV/Excel export
-   Print-friendly reports
-   PDF/printable invoice workflow

------------------------------------------------------------------------

# 4. Project Architecture

Recommended Django structure:

``` text
service_management/
│
├── manage.py
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── accounts/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   └── admin.py
│
├── customers/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   └── admin.py
│
├── services/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   └── admin.py
│
├── ledger/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
│
├── notifications/
│   ├── models.py
│   ├── services/
│   │   └── whatsapp.py
│   └── admin.py
│
├── dashboard/
│   ├── views.py
│   └── urls.py
│
├── templates/
│   ├── base.html
│   ├── landing/
│   ├── accounts/
│   ├── dashboard/
│   ├── customers/
│   ├── services/
│   ├── ledger/
│   └── reports/
│
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
├── media/
│
├── .env
├── .env.example
├── requirements.txt
└── README.md
```

The exact app structure can be adjusted during development, but keep
responsibilities separated.

------------------------------------------------------------------------

# 5. Public Website

The public website is accessible without login.

## Main URL

``` text
/
```

## Pages

``` text
/
├── Home
├── About
├── Services
├── Portfolio
└── Contact
```

------------------------------------------------------------------------

## 5.1 Home Page

The home page should introduce:

**ROBO DIGITAL COMPUTERS**

Main description:

> Computer Sales, Service & Digital Solutions

The page should contain:

-   Company logo
-   Hero section
-   Company introduction
-   Services
-   Why choose us
-   Portfolio preview
-   Service Management module
-   Contact section
-   Footer

The uploaded ROBO DIGITAL COMPUTERS logo is the official branding
source.

Do not create a replacement logo.

------------------------------------------------------------------------

# 6. Company Services

The public website must represent the actual company services.

## 6.1 Computer Sales & Service

Computer sales, maintenance, troubleshooting and repair.

## 6.2 Laptop Chip Level Service

Advanced laptop motherboard and chip-level diagnosis and repair.

## 6.3 CCTV Camera Installation

CCTV installation, configuration and maintenance.

## 6.4 Printer & UPS Sales & Service

Printer and UPS sales, repair and maintenance.

## 6.5 Xerox & Color Print & Scan

Xerox, color printing, scanning and document services.

## 6.6 All Type Online Work

Online applications, digital services and related online assistance.

## 6.7 Tamil & English Typing

Tamil and English typing and document preparation.

------------------------------------------------------------------------

# 7. Service Management Login

The internal system is protected.

URL:

``` text
/service/login/
```

There is **no public registration**.

Only an administrator can create staff accounts.

Authentication uses Django's built-in authentication system.

Login:

``` text
Username
Password
```

After successful login:

``` text
/service/dashboard/
```

Unauthorized users must be redirected to the login page.

------------------------------------------------------------------------

# 8. User Roles

## 8.1 Admin

Admin can:

-   Create staff
-   Update staff
-   Disable staff
-   View all services
-   Manage customers
-   Manage service records
-   View all ledgers
-   View expenses
-   View payments
-   Generate reports
-   Download monthly reports
-   Download yearly reports
-   Manage system settings
-   Access Django Admin
-   View notification history

## 8.2 Staff

Staff can:

-   Login
-   Create service inward
-   View service records
-   Search services
-   Update service status
-   Add diagnosis
-   Add work progress
-   Add expenses
-   Add payments
-   Mark service completed
-   Generate/view permitted bills
-   View customer information

Staff cannot:

-   Create administrator accounts
-   Access sensitive system settings
-   Download admin-only reports
-   Perform restricted destructive operations

------------------------------------------------------------------------

# 9. Dashboard

URL:

``` text
/service/dashboard/
```

The dashboard provides a quick overview of business activity.

## Statistics

Show:

-   Total Customers
-   Total Services
-   Pending Services
-   In Progress
-   Completed
-   Delivered
-   Total Revenue
-   Outstanding Amount

## Service Status

Display:

``` text
Pending
In Progress
Completed
Delivered
```

## Device Statistics

Display:

``` text
Laptop
Desktop
Printer
Other
```

## Recent Services

Display:

  Service ID   Customer   Device   Status   Created By   Date
  ------------ ---------- -------- -------- ------------ ------

## Overdue Services

Show services that have remained pending/in progress beyond the expected
completion date.

------------------------------------------------------------------------

# 10. Service Inward

The Service Inward is the most important part of the system.

URL:

``` text
/service/inward/
```

It represents the moment a customer gives a device to the company.

------------------------------------------------------------------------

# 11. Service ID

Every service receives a unique ID.

Example:

``` text
SRV-2026-00001
SRV-2026-00002
SRV-2026-00003
```

The ID should be generated automatically.

Users should not manually enter the Service ID.

------------------------------------------------------------------------

# 12. Customer Information

## Important Business Rule

Customers do **not** create their own accounts.

There is:

- No customer registration
- No customer login
- No customer dashboard
- No customer self-service account creation

The **staff member creates the customer record** when the customer brings a device to ROBO DIGITAL COMPUTERS.

The `customers/` Django app is therefore an **internal Customer Management module**, used by authorized staff and administrators.

## 12.1 Customer Creation Workflow

The preferred workflow is to create/find a customer directly from the **New Service Inward** process.

```text
Staff Login
    ↓
New Service Inward
    ↓
Search Customer by Phone / Name
    ↓
Customer Found?
   /       \
 YES       NO
  ↓         ↓
Select    Create New Customer
Customer       ↓
   \          /
    \        /
      ↓     ↓
    Service Details
          ↓
     Create Service
```

## 12.2 Search Existing Customer First

Before creating a new customer, staff should search using:

- Phone number
- Customer name
- Customer ID

The system should help prevent duplicate customers.

Example:

```text
New Service Inward
--------------------------------
Customer Search

Phone: [9876543210] [Search]

Existing Customer:
Ravi Kumar
9876543210

[Select Customer]
```

If the customer does not exist:

```text
No customer found.

[+ Create New Customer]
```

## 12.3 Create New Customer

Staff enters:

- Customer Name
- Phone
- Alternate Phone
- Email
- Address

The system generates a Customer ID automatically:

```text
CUS-2026-00001
```

After creation, the system should automatically return to the Service Inward form with the newly created customer selected.

## 12.4 Create Service Immediately

After selecting/creating the customer, staff continues with device information and complaint details.

The system then generates a unique Service ID such as:

```text
SRV-2026-00001
```

and automatically records the logged-in staff member as `created_by`.

## 12.5 Customer Management Page

The separate Customer Management page is still required, but it is an **internal staff/admin management page**.

URL:

```text
/service/customers/
```

Staff/Admin can:

- Search customers
- View customer details
- Edit customer information
- View service history
- View payment history related to services
- View total number of services
- View pending/completed/delivered services

Example:

```text
Customer: Ravi Kumar
Customer ID: CUS-2026-00001
Phone: 9876543210

Total Services: 8
Pending: 1
In Progress: 1
Completed: 2
Delivered: 4
```

## 12.6 Customer-to-Service Relationship

One customer can have multiple services.

```text
Customer
    │
    ├── Service 1
    │      └── Ledger
    │
    ├── Service 2
    │      └── Ledger
    │
    └── Service 3
           └── Ledger
```

Database relationship:

```text
One Customer → Many Services
```

The `Customer` model belongs to the `customers/` app.

The `Service` model belongs to the `services/` app.

The relationship should be implemented using a Django `ForeignKey`.

## 12.7 Customer App Responsibility

The `customers/` app is responsible for:

- Customer database
- Customer creation by staff
- Customer editing
- Customer search
- Customer details
- Customer service history

It is **not** responsible for:

- Customer authentication
- Customer registration
- Customer portal
- Service workflow
- Service ledger
- Invoice generation

Those responsibilities belong to other modules.

# 13. Device Information

Service devices can be:

``` text
Laptop
Desktop
Printer
Other
```

Store:

-   Device Type
-   Brand
-   Model
-   Serial Number
-   Asset Number
-   Physical Condition

Example:

``` text
Device Type: Laptop
Brand: Dell
Model: Inspiron 15
Serial Number: XXXXX
```

------------------------------------------------------------------------

# 14. Accessories

Record everything received with the device.

Possible accessories:

-   Charger
-   Adapter
-   Battery
-   Power Cable
-   Mouse
-   Keyboard
-   Bag
-   Other

This is important because accessories must be returned with the device.

------------------------------------------------------------------------

# 15. Customer Complaint

Record:

-   Customer Complaint
-   Initial Diagnosis
-   Physical Condition
-   Technician Notes

Example:

``` text
Customer Complaint:
Laptop is not turning on.

Initial Diagnosis:
Power section needs inspection.
```

------------------------------------------------------------------------

# 16. Service Information

Store:

-   Service Type
-   Priority
-   Expected Completion Date
-   Estimated Cost
-   Created By
-   Created Date

Initial status:

``` text
Pending
```

------------------------------------------------------------------------

# 17. Automatic Staff Assignment

The logged-in user is automatically recorded.

Example:

``` text
Created By: Arun
Created At: 21-Aug-2026 10:30 AM
```

The staff member must not manually select themselves.

Also track:

``` text
Last Updated By
Last Updated At
```

------------------------------------------------------------------------

# 18. Service Status Workflow

The standard workflow is:

``` text
Pending
   ↓
In Progress
   ↓
Completed
   ↓
Delivered
```

Optional status:

``` text
Cancelled
```

Each status change must create a history/ledger entry.

Example:

``` text
21-Aug-2026 10:30
Pending → In Progress
Updated By: Staff Name
```

------------------------------------------------------------------------

# 19. Service Details

URL example:

``` text
/service/SRV-2026-00001/
```

The service detail page should show:

### Customer

-   Name
-   Phone
-   Address

### Device

-   Type
-   Brand
-   Model
-   Serial Number
-   Accessories

### Complaint

-   Customer complaint
-   Diagnosis
-   Technician notes

### Status

Current service status.

### Work Progress

All work updates.

### Expenses

Parts and other expenses.

### Payments

All payments.

### Ledger

Complete service history.

### Bill

Invoice information.

### Notifications

WhatsApp notification history.

------------------------------------------------------------------------

# 20. Work Progress

Technicians should be able to add work updates.

Example:

``` text
Date: 21-Aug-2026

Progress:
Laptop motherboard inspected.

Result:
Power IC suspected faulty.

Updated By:
Staff Name
```

Multiple progress records should be allowed.

------------------------------------------------------------------------

# 21. Expense Management

Expenses belong to a service.

Example:

``` text
Keyboard Replacement     ₹1500
SSD                      ₹3500
Power IC                  ₹800
Technician Expense        ₹300
```

Expense fields:

-   Service
-   Expense Type
-   Description
-   Amount
-   Date
-   Added By

Use Django DecimalField for money.

Never use floating point for financial calculations.

------------------------------------------------------------------------

# 22. Payment Management

A service can have one or multiple payments.

Fields:

-   Service
-   Amount
-   Payment Method
-   Payment Date
-   Reference Number
-   Notes
-   Recorded By

Payment methods:

``` text
Cash
UPI
Card
Bank Transfer
Other
```

Calculate:

``` text
Total Service Amount
Total Paid
Balance
```

Payment status:

``` text
Unpaid
Partially Paid
Paid
```

------------------------------------------------------------------------

# 23. Service Ledger

The ledger is the complete history of a service.

Example:

``` text
Service Created
      ↓
Diagnosis Started
      ↓
Work Started
      ↓
Part Added
      ↓
Expense Added
      ↓
Payment Received
      ↓
Work Completed
      ↓
Bill Generated
      ↓
Customer Notified
      ↓
Device Delivered
```

Each ledger record should contain:

-   Service
-   Date
-   Time
-   Action
-   Description
-   Staff
-   Amount if applicable

The ledger should be append-oriented. Important historical events should
not be silently overwritten.

------------------------------------------------------------------------

# 24. Bill Generation

A bill can be generated only after the service is marked:

``` text
Completed
```

The bill should contain:

## Company

-   Logo
-   ROBO DIGITAL COMPUTERS
-   Address
-   Phone
-   Email
-   GST details if applicable

## Customer

-   Name
-   Phone
-   Address

## Service

-   Service ID
-   Service Date
-   Completion Date
-   Device
-   Brand
-   Model
-   Serial Number

## Charges

``` text
Service Charge
Parts
Other Charges
Discount
Total
Paid
Balance
```

Provide:

``` text
Print Bill
Download Bill
```

The invoice should be designed for A4 printing and normal
thermal/receipt printing can be considered later if required.

------------------------------------------------------------------------

# 25. Service Completion

When a staff member marks a service as Completed:

The system should:

1.  Save completion date/time.
2.  Create a ledger entry.
3.  Calculate final amount.
4.  Make bill generation available.
5.  Trigger the completion WhatsApp notification.
6.  Change the service state to Completed.

The device can later be marked:

``` text
Delivered
```

when the customer collects it.

------------------------------------------------------------------------

# 26. Customer Management

URL:

``` text
/service/customers/
```

Features:

-   Add customer
-   Edit customer
-   Search customer
-   Filter customer
-   View customer
-   View service history

Customer detail should show:

``` text
Customer Name
Phone
Total Services
Pending Services
Completed Services
Delivered Services
Total Amount
Total Paid
Outstanding
```

And all related services.

------------------------------------------------------------------------

# 27. Search and Filtering

Service search should support:

-   Service ID
-   Customer name
-   Phone
-   Serial number
-   Model

Filters:

-   Status
-   Device type
-   Date
-   Staff
-   Priority

Use pagination for large datasets.

------------------------------------------------------------------------

# 28. Admin Reports

Only Admin can download management reports.

## Monthly Report

Admin selects:

``` text
Month
Year
```

The report contains:

-   Service ID
-   Customer
-   Device
-   Service date
-   Completion date
-   Status
-   Staff
-   Service amount
-   Expenses
-   Payments
-   Balance

## Yearly Report

Admin selects:

``` text
Year
```

Show the same information for the selected year.

Totals:

``` text
Total Services
Total Revenue
Total Expenses
Total Collected
Total Outstanding
```

Export options:

-   CSV
-   Excel if implemented
-   Print-friendly report

------------------------------------------------------------------------

# 29. WhatsApp Notifications

The system should automatically notify customers through the company's
official WhatsApp Business account.

There are two important notifications.

## 29.1 Service Inward Notification

When a service is created:

``` text
Dear {customer_name},

Your device has been received for service.

Service ID: {service_id}
Device: {device}
Brand/Model: {brand_model}
Complaint: {complaint}

We will update you once the service is completed.

Thank you,
ROBO DIGITAL COMPUTERS
```

## 29.2 Service Completed Notification

When service becomes Completed:

``` text
Dear {customer_name},

Your service has been completed.

Service ID: {service_id}
Device: {device}
Total Amount: ₹{amount}
Balance: ₹{balance}

Your device is ready for delivery/collection.

Thank you,
ROBO DIGITAL COMPUTERS
```

------------------------------------------------------------------------

# 30. WhatsApp Architecture

Do not place API credentials directly in Python code.

Use `.env`.

Example:

``` env
WHATSAPP_API_URL=
WHATSAPP_ACCESS_TOKEN=
WHATSAPP_PHONE_NUMBER_ID=
WHATSAPP_BUSINESS_ACCOUNT_ID=
```

Create a dedicated service:

``` text
notifications/
└── services/
    └── whatsapp.py
```

Workflow:

``` text
Service Created
      ↓
Notification Service
      ↓
WhatsApp Business API
      ↓
Customer WhatsApp
```

Store every notification attempt.

Notification fields:

-   Service
-   Customer
-   Type
-   Message
-   Status
-   Sent At
-   Error Message

Statuses:

``` text
Pending
Sent
Failed
```

If WhatsApp fails, the service creation/completion must still succeed.

The failure should be recorded so it can be retried.

Use the official WhatsApp Business Platform/API or an authorized
provider. Do not use WhatsApp Web scraping or unofficial automation.

------------------------------------------------------------------------

# 31. Database Design

Recommended models:

``` text
User
Customer
Service
ServiceAccessory
ServiceStatusHistory
ServiceProgress
ServiceExpense
ServicePayment
ServiceLedger
Invoice
WhatsAppNotification
```

Relationships:

``` text
User
  │
  ├── created services
  ├── updated services
  ├── ledger entries
  └── expenses/payments

Customer
  │
  └── Services
        ├── Status History
        ├── Progress
        ├── Expenses
        ├── Payments
        ├── Ledger
        ├── Invoice
        └── Notifications
```

------------------------------------------------------------------------

# 32. Suggested Service Model

Conceptually:

``` text
Service
-------------------------
service_id
customer
device_type
brand
model
serial_number
asset_number
complaint
initial_diagnosis
physical_condition
priority
status
expected_completion_date
estimated_cost
final_amount
created_by
updated_by
created_at
updated_at
completed_at
delivered_at
```

Do not copy this blindly. Design the final Django model based on actual
requirements.

------------------------------------------------------------------------

# 33. Suggested Customer Model

``` text
Customer
-------------------------
customer_id
name
phone
alternate_phone
email
address
created_at
updated_at
```

Phone number should be indexed/searchable.

------------------------------------------------------------------------

# 34. Suggested Expense Model

``` text
ServiceExpense
-------------------------
service
expense_type
description
amount
expense_date
created_by
created_at
```

------------------------------------------------------------------------

# 35. Suggested Payment Model

``` text
ServicePayment
-------------------------
service
amount
payment_method
reference_number
payment_date
notes
recorded_by
created_at
```

------------------------------------------------------------------------

# 36. Suggested Ledger Model

``` text
ServiceLedger
-------------------------
service
action
description
amount
created_by
created_at
```

------------------------------------------------------------------------

# 37. Security

The system contains customer and financial information.

Implement:

-   Django authentication
-   Role-based authorization
-   CSRF protection
-   Password hashing
-   Login protection
-   Session management
-   Server-side validation
-   Django ORM
-   XSS-safe templates
-   Secure file handling
-   Environment variables
-   Database credentials outside source code

Never commit:

``` text
.env
database passwords
SECRET_KEY
WhatsApp access tokens
API credentials
```

Add them to `.gitignore`.

------------------------------------------------------------------------

# 38. Django Admin

Django Admin should be configured for administrators.

Manage:

-   Users
-   Customers
-   Services
-   Service status history
-   Progress
-   Expenses
-   Payments
-   Ledgers
-   Invoices
-   WhatsApp notifications

Add:

-   Search
-   Filters
-   Ordering
-   Useful list displays
-   Read-only timestamps

------------------------------------------------------------------------

# 39. User Interface

The management system should have:

### Sidebar

``` text
Dashboard

SERVICE MANAGEMENT
- Service Inward
- All Services
- Pending
- In Progress
- Completed
- Delivered

CUSTOMERS
- Customers

LEDGER
- Service Ledger

REPORTS
- Monthly
- Yearly

ADMIN
- Staff
- Settings
- Django Admin

Logout
```

### Top Bar

Display:

``` text
ROBO DIGITAL COMPUTERS
Logged in user
Notifications
Profile
Logout
```

------------------------------------------------------------------------

# 40. UI Design Principles

The system should not look like a basic CRUD project.

Use:

-   Bootstrap 5
-   Bootstrap Icons
-   Responsive tables
-   Cards
-   Badges
-   Modals
-   Toast messages
-   Confirmation dialogs
-   Breadcrumbs
-   Clean forms
-   Good spacing
-   Mobile responsiveness

Status badges:

``` text
Pending      → Warning
In Progress  → Primary
Completed    → Success
Delivered    → Secondary
Cancelled    → Danger
```

Always show the status text, not only color.

------------------------------------------------------------------------

# 41. Environment Configuration

Create:

``` text
.env
.env.example
```

Example:

``` env
DEBUG=True
SECRET_KEY=change-this

DB_NAME=service_management
DB_USER=root
DB_PASSWORD=
DB_HOST=localhost
DB_PORT=3306

WHATSAPP_API_URL=
WHATSAPP_ACCESS_TOKEN=
WHATSAPP_PHONE_NUMBER_ID=
WHATSAPP_BUSINESS_ACCOUNT_ID=
```

`.env` must not be committed to Git.

------------------------------------------------------------------------

# 42. Installation

## Step 1 --- Create Virtual Environment

Windows:

``` bash
python -m venv venv
```

Activate:

``` bash
venv\Scripts\activate
```

Linux/macOS:

``` bash
python3 -m venv venv
source venv/bin/activate
```

------------------------------------------------------------------------

# 43. Install Django

``` bash
pip install django==5.2.5
```

Install other required packages as the project develops.

Finally create:

``` text
requirements.txt
```

using:

``` bash
pip freeze > requirements.txt
```

------------------------------------------------------------------------

# 44. MySQL Setup

Create a MySQL database:

``` sql
CREATE DATABASE service_management;
```

Configure Django to use MySQL.

Example:

``` env
DB_NAME=service_management
DB_USER=root
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3306
```

Never place the real password inside Git-tracked source code.

------------------------------------------------------------------------

# 45. Django Migrations

After creating models:

``` bash
python manage.py makemigrations
python manage.py migrate
```

Create an admin user:

``` bash
python manage.py createsuperuser
```

Run:

``` bash
python manage.py runserver
```

Open:

``` text
http://127.0.0.1:8000/
```

------------------------------------------------------------------------

# 46. Development Strategy

Do not try to build everything at once.

Build in this order:

``` text
1. Project setup
2. Database
3. Authentication
4. Public landing page
5. Customer model
6. Service model
7. Service inward
8. Service list/detail
9. Status workflow
10. Ledger
11. Expenses
12. Payments
13. Invoice
14. Reports
15. WhatsApp
16. UI polishing
17. Security
18. Testing
19. Documentation
```

------------------------------------------------------------------------

# 47. Two-Week Development Plan

The goal is to build the first complete working version in **14 days**.

The project should be developed using your own knowledge, with AI used
as a guide/debugging assistant rather than simply generating the whole
application.

------------------------------------------------------------------------

## DAY 1 --- Project Setup

Learn and implement:

-   Django project creation
-   Virtual environment
-   MySQL connection
-   `.env`
-   Git/GitHub
-   Django settings
-   Static/media configuration
-   Base template

Target:

``` text
Django + MySQL working
```

------------------------------------------------------------------------

## DAY 2 --- Authentication

Build:

-   Login
-   Logout
-   User authentication
-   Admin account
-   Staff account
-   Permission structure

Target:

``` text
Login → Dashboard
```

------------------------------------------------------------------------

## DAY 3 --- Public Website

Build:

-   Navbar
-   Hero
-   About
-   Services
-   Portfolio
-   Contact
-   Footer
-   Company logo

Target:

``` text
Professional landing page
```

------------------------------------------------------------------------

## DAY 4 --- Customer Management

Create:

- Customer model
- Customer form
- Customer list
- Customer search
- Customer detail
- Customer service history
- Staff-created customer workflow
- Customer search from New Service Inward
- Duplicate-customer prevention

Important workflow:

```text
New Service Inward
        ↓
Search Existing Customer
        ↓
Found → Select Customer
        ↓
Not Found → Create Customer
        ↓
Continue Service Inward
```

There is no customer registration or customer login.

Target:

```text
Staff can create/find a customer and immediately use that customer for a service.
```

------------------------------------------------------------------------

## DAY 5 --- Service Inward

Create:

-   Service model
-   Automatic Service ID
-   Customer selection
-   Device information
-   Accessories
-   Complaint
-   Priority
-   Expected completion
-   Created By

Target:

``` text
Create Service Inward successfully
```

------------------------------------------------------------------------

## DAY 6 --- Service Management

Build:

-   Service list
-   Search
-   Filters
-   Service detail
-   Edit service
-   Status update

Workflow:

``` text
Pending
↓
In Progress
↓
Completed
↓
Delivered
```

Target:

``` text
Complete service workflow
```

------------------------------------------------------------------------

## DAY 7 --- Service Ledger

Build:

-   Status history
-   Work progress
-   Timeline
-   Service ledger

Target:

``` text
Every important action is recorded
```

------------------------------------------------------------------------

## DAY 8 --- Expenses & Payments

Build:

-   Expense form
-   Expense list
-   Payment form
-   Payment history
-   Total amount
-   Paid amount
-   Balance
-   Payment status

Target:

``` text
Financial tracking working
```

------------------------------------------------------------------------

## DAY 9 --- Invoice

Build:

-   Invoice model
-   Invoice page
-   Company branding
-   Customer details
-   Service details
-   Charges
-   Payment
-   Balance
-   Print

Rule:

``` text
Only Completed services can generate invoices.
```

------------------------------------------------------------------------

## DAY 10 --- Dashboard

Build:

-   Statistics
-   Recent services
-   Status distribution
-   Device statistics
-   Overdue services
-   Revenue
-   Outstanding amount

Target:

``` text
Useful management dashboard
```

------------------------------------------------------------------------

## DAY 11 --- Reports

Build:

-   Monthly report
-   Yearly report
-   CSV export
-   Print-friendly report
-   Admin-only access

Target:

``` text
Admin can download business reports
```

------------------------------------------------------------------------

## DAY 12 --- WhatsApp Integration

First build the internal notification architecture.

Create:

``` text
notifications/
    models.py
    services/
        whatsapp.py
```

Implement:

``` text
Service Created
       ↓
Notification Service
       ↓
WhatsApp API
```

Then:

``` text
Service Completed
       ↓
Notification Service
       ↓
WhatsApp API
```

If API credentials are not available yet, implement a mock/test
notification provider so the rest of the project remains testable.

------------------------------------------------------------------------

## DAY 13 --- Security & Testing

Test:

-   Login protection
-   Staff permissions
-   Admin permissions
-   CSRF
-   Invalid forms
-   Duplicate customers
-   Duplicate service IDs
-   Payment calculations
-   Invoice rules
-   Report permissions
-   WhatsApp failures
-   Status transitions

Also test the complete workflow manually.

------------------------------------------------------------------------

## DAY 14 --- Final Integration & Polish

Complete:

-   UI polishing
-   Responsive design
-   Error pages
-   Empty states
-   Loading states
-   Toast messages
-   Confirmation dialogs
-   Logo
-   Company branding
-   README
-   `.env.example`
-   Git cleanup

Final workflow test:

``` text
Customer
   ↓
Service Inward
   ↓
Staff Assigned
   ↓
Diagnosis
   ↓
In Progress
   ↓
Expenses
   ↓
Payments
   ↓
Completed
   ↓
Invoice
   ↓
WhatsApp
   ↓
Delivered
```

------------------------------------------------------------------------

# 48. What You Should Learn During This Project

Do not only copy code.

You should understand:

## Django

-   Project vs App
-   URLs
-   Views
-   Templates
-   Models
-   ORM
-   Migrations
-   Forms
-   Authentication
-   Permissions
-   Admin
-   Static files
-   Media files
-   Signals
-   Transactions

## MySQL

-   Database
-   Tables
-   Primary keys
-   Foreign keys
-   Relationships
-   Indexes
-   Queries
-   Constraints

## Frontend

-   HTML
-   CSS
-   Bootstrap
-   JavaScript
-   Forms
-   AJAX/fetch where useful
-   DOM manipulation

## Software Engineering

-   MVC/MVT
-   Separation of concerns
-   Reusable components
-   Validation
-   Error handling
-   Git
-   Environment variables
-   Testing
-   Debugging

------------------------------------------------------------------------

# 49. How AI Should Be Used During Development

Use AI as your development mentor.

Do not start by asking:

> "Generate the entire project."

Instead, work module by module.

Example:

``` text
I am building the Customer model.
Explain what fields I need and why.
Do not write the complete code yet.
```

Then implement it yourself.

If you get an error:

``` text
Here is my model.
Here is the error.
Explain why it happens and guide me to fix it.
```

For difficult sections:

``` text
Explain the logic first.
Then give me a small example.
Then let me implement it.
```

This approach will help you understand the project instead of only
copying generated code.

------------------------------------------------------------------------

# 50. Recommended Development Cycle

For every feature:

``` text
Understand
   ↓
Design
   ↓
Create Model
   ↓
Migration
   ↓
Create Form
   ↓
Create View
   ↓
Create URL
   ↓
Create Template
   ↓
Test
   ↓
Fix Errors
   ↓
Commit to Git
```

Example:

``` text
Customer Management
        ↓
Understand requirement
        ↓
Customer model
        ↓
Migration
        ↓
Customer form
        ↓
Customer views
        ↓
Customer URLs
        ↓
Customer templates
        ↓
Test CRUD
        ↓
Git commit
```

------------------------------------------------------------------------

# 51. Git Commit Strategy

Commit after completing each major module.

Example:

``` text
git commit -m "Setup Django project"
git commit -m "Configure MySQL database"
git commit -m "Add authentication"
git commit -m "Create public landing page"
git commit -m "Add customer management"
git commit -m "Add service inward"
git commit -m "Add service workflow"
git commit -m "Add service ledger"
git commit -m "Add expense and payment tracking"
git commit -m "Add invoice generation"
git commit -m "Add dashboard"
git commit -m "Add reports"
git commit -m "Add WhatsApp notification service"
git commit -m "Complete security and testing"
```

------------------------------------------------------------------------

# 52. Minimum Viable Product

If the 14-day deadline becomes difficult, prioritize these features:

### Must Have

-   Login
-   Staff authentication
-   Customer management
-   Service inward
-   Service ID
-   Device information
-   Service status
-   Created By
-   Service details
-   Service ledger
-   Expenses
-   Payments
-   Invoice
-   Dashboard
-   Monthly/yearly report

### Can Be Added After MVP

-   WhatsApp API production integration
-   Advanced analytics
-   PDF generation improvements
-   Advanced search
-   Automated reminders
-   Customer portal
-   Online service tracking
-   Inventory management
-   Spare parts management

Do not sacrifice the core service workflow just to add extra features.

------------------------------------------------------------------------

# 53. Future Improvements

The system can later be expanded with:

-   Customer login
-   Customer service tracking
-   QR code on service receipt
-   Service status public tracking
-   Spare parts inventory
-   Purchase management
-   Supplier management
-   Technician performance reports
-   Advanced revenue analytics
-   Automatic overdue reminders
-   Email notifications
-   WhatsApp templates
-   Online payment
-   GST invoice support
-   Multi-branch support
-   Backup system
-   Cloud deployment
-   Mobile application

------------------------------------------------------------------------

# 54. Final Success Criteria

The project is considered a successful first version when this complete
scenario works:

``` text
Admin creates staff
        ↓
Staff logs in
        ↓
Staff searches/creates customer
        ↓
Staff creates service inward
        ↓
System generates Service ID
        ↓
System records staff automatically
        ↓
Customer receives inward notification
        ↓
Staff updates service to In Progress
        ↓
Staff records diagnosis/work
        ↓
Staff records expenses
        ↓
Staff records customer payment
        ↓
Staff marks service Completed
        ↓
System calculates final amount
        ↓
Invoice becomes available
        ↓
Customer receives completion notification
        ↓
Customer collects device
        ↓
Staff marks Delivered
        ↓
Service history remains available
        ↓
Admin can see it in reports
```

------------------------------------------------------------------------

# 55. Final Project Vision

ROBO DIGITAL COMPUTERS Service Management System should become the
central system for managing the company's service operations.

The system should make it easy for staff to answer:

-   Which device is currently in service?
-   Who is the customer?
-   What problem does the device have?
-   Which staff member created the service?
-   What work has been completed?
-   What parts were used?
-   How much was spent?
-   How much did the customer pay?
-   What is the balance?
-   Is the device completed?
-   Has the customer been notified?
-   Has the device been delivered?
-   What services were completed this month?
-   How much revenue was generated?
-   What services are overdue?

The final system should be **simple for staff to use, reliable for
business records, secure for customer information and scalable for
future development.**

------------------------------------------------------------------------

# 56. Development Rule for This Project

Build the project **yourself with guidance**.

For every module, understand:

``` text
WHY → WHAT → HOW → CODE → TEST
```

Do not move to the next module until the current module works.

The target for the first 14 days is not a perfect enterprise system.

The target is:

> **A complete, working, understandable Service Management System that
> you can explain and maintain yourself.**
