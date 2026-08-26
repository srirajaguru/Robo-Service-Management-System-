import datetime
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from accounts.models import StaffProfile
from customers.models import Customer
from services.models import Service, ServiceHistory, ServiceProgress
from ledger.models import Expense, Payment, LedgerEntry, Invoice
from notification.models import Notification


class Command(BaseCommand):
    help = 'Seeds initial users, customers, services, expenses, payments, and notifications for ROBO DIGITAL COMPUTERS.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Seeding ROBO DIGITAL COMPUTERS Service Management data..."))

        # 1. Create Superuser / Admin
        admin_user, created = User.objects.get_or_create(username='admin', defaults={'email': 'admin@robodigital.com', 'first_name': 'Admin Head', 'is_staff': True, 'is_superuser': True})
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            self.stdout.write(self.style.SUCCESS("Created admin user: admin / admin123"))
        
        admin_profile, _ = StaffProfile.objects.get_or_create(
            user=admin_user,
            defaults={'name': 'System Administrator', 'phone_number': '8122227042', 'role': 'Admin', 'is_active': True}
        )

        # 2. Create Staff Members
        staff1_user, created1 = User.objects.get_or_create(username='arun', defaults={'email': 'arun@robodigital.com', 'first_name': 'Arun Kumar', 'is_staff': True})
        if created1:
            staff1_user.set_password('staff123')
            staff1_user.save()
        staff1, _ = StaffProfile.objects.get_or_create(
            user=staff1_user,
            defaults={'name': 'Arun Kumar (Chip Level Specialist)', 'phone_number': '8122227074', 'role': 'Staff', 'is_active': True}
        )

        staff2_user, created2 = User.objects.get_or_create(username='priya', defaults={'email': 'priya@robodigital.com', 'first_name': 'Priya S.', 'is_staff': True})
        if created2:
            staff2_user.set_password('staff123')
            staff2_user.save()
        staff2, _ = StaffProfile.objects.get_or_create(
            user=staff2_user,
            defaults={'name': 'Priya S. (Service Desk & Accounts)', 'phone_number': '9443312345', 'role': 'Staff', 'is_active': True}
        )

        # 3. Create Sample Customers in Musiri / Trichy
        customers_data = [
            {'name': 'Ramesh Kannan', 'phone_number': '9876543210', 'alternate_phone': '9876543211', 'email': 'ramesh.k@gmail.com', 'address': '12 Car Street, Musiri, Trichy - 621211'},
            {'name': 'Dr. S. Meenakshi', 'phone_number': '9842455667', 'alternate_phone': '', 'email': 'meenakshi.clinic@yahoo.com', 'address': 'Opp. Govt Hospital, Trichy Main Road, Musiri'},
            {'name': 'Balaji Textiles (Mr. Balaji)', 'phone_number': '9442233445', 'alternate_phone': '04326261234', 'email': 'balajitex@gmail.com', 'address': '45 Bazaar Street, Musiri, Trichy'},
            {'name': 'Kavitha Murugan', 'phone_number': '9789012345', 'alternate_phone': '', 'email': 'kavitha.m@outlook.com', 'address': '8/2 Annai Nagar, Thottiyam Road, Musiri'},
            {'name': 'Greenland School (Principal)', 'phone_number': '9865011223', 'alternate_phone': '9865011224', 'email': 'info@greenlandschool.edu.in', 'address': 'Vellur Bypass, Musiri Taluk'},
            {'name': 'Senthil Nathan', 'phone_number': '9487123987', 'alternate_phone': '', 'email': 'senthil.nathan@gmail.com', 'address': '22 Kattuputhur Road, Musiri'},
        ]

        created_customers = []
        for cdata in customers_data:
            cust, _ = Customer.objects.get_or_create(phone_number=cdata['phone_number'], defaults=cdata)
            created_customers.append(cust)

        # 4. Create Sample Services across various stages
        services_data = [
            {
                'customer': created_customers[0],
                'device_type': 'Laptop',
                'brand': 'Dell',
                'model': 'Inspiron 15 3511 (Core i5 11th Gen)',
                'serial_number': 'DLL-INSP-88231',
                'asset_number': '',
                'physical_condition': 'Light scratches on bottom panel, display intact',
                'accessories': 'Original 65W Dell Adapter, Laptop Bag',
                'complaint': 'Laptop suddenly dead, not turning on with charger. Power LED blinking amber 3 times.',
                'initial_diagnosis': 'Power management IC and shorted 19V rail capacitor suspected.',
                'technician_notes': 'Motherboard chip level inspection required. Quoted approx 2500 - 3500.',
                'priority': 'High',
                'status': 'In Progress',
                'expected_completion_date': timezone.localdate() + datetime.timedelta(days=1),
                'estimated_cost': Decimal('3200.00'),
                'service_charge': Decimal('1500.00'),
                'discount': Decimal('0.00'),
                'created_by': staff1,
                'updated_by': staff1,
                'progress_notes': ['Disassembled laptop and cleaned dust.', 'Found shorted capacitor on 19V power rail near charging IC. Replaced capacitor.', 'Motherboard powered on successfully. Stress testing in progress.'],
                'expenses': [('Motherboard Chip', 'Power Section SMD Capacitor & Mosfet', Decimal('450.00'))],
                'payments': [(Decimal('1000.00'), 'UPI', 'UPI-9876543210-01', 'Advance paid during inward')],
            },
            {
                'customer': created_customers[1],
                'device_type': 'Printer',
                'brand': 'Epson',
                'model': 'EcoTank L3110 All-in-One',
                'serial_number': 'EPS-L3110-99432',
                'asset_number': 'CLINIC-PRN-01',
                'physical_condition': 'Good condition, original ink bottles present',
                'accessories': 'Power Cable, USB Printer Cable',
                'complaint': 'Paper jam error repeating and black ink not printing clearly (lines broken).',
                'initial_diagnosis': 'Print head nozzle clogging and paper feed roller roller wear.',
                'technician_notes': 'Perform ultrasonic head cleaning and roller service.',
                'priority': 'Medium',
                'status': 'Completed',
                'expected_completion_date': timezone.localdate() - datetime.timedelta(days=1),
                'estimated_cost': Decimal('1200.00'),
                'service_charge': Decimal('800.00'),
                'discount': Decimal('100.00'),
                'created_by': staff2,
                'updated_by': staff1,
                'completed_at': timezone.now() - datetime.timedelta(hours=4),
                'progress_notes': ['Nozzle check performed. Deep ultrasonic cleaning completed.', 'Tested 50 color and black test prints. Print quality crystal clear.'],
                'expenses': [('Consumable', 'Printhead Cleaning Solution & Pad replacement', Decimal('250.00'))],
                'payments': [(Decimal('950.00'), 'Cash', '', 'Full payment settled')],
            },
            {
                'customer': created_customers[2],
                'device_type': 'CCTV',
                'brand': 'CP Plus',
                'model': '8-Channel DVR with 5TB Storage',
                'serial_number': 'CP-DVR8-5512',
                'asset_number': 'SHOP-DVR-01',
                'physical_condition': 'Dust accumulated in vents, HDD attached',
                'accessories': '12V 5A Power Supply Adapter, USB Mouse, HDMI Cable',
                'complaint': 'DVR beeping continuously and Cameras 3 & 4 showing Video Loss.',
                'initial_diagnosis': 'SMPS channel power drop and BNC connector loose connection.',
                'technician_notes': 'Tested DVR onboard ports; replace CCTV SMPS unit.',
                'priority': 'Urgent',
                'status': 'Delivered',
                'expected_completion_date': timezone.localdate() - datetime.timedelta(days=3),
                'estimated_cost': Decimal('2200.00'),
                'service_charge': Decimal('700.00'),
                'discount': Decimal('0.00'),
                'created_by': staff1,
                'updated_by': staff1,
                'completed_at': timezone.now() - datetime.timedelta(days=2),
                'delivered_at': timezone.now() - datetime.timedelta(days=1),
                'progress_notes': ['Replaced 8-channel CCTV SMPS with original CP Plus power supply unit.', 'All 8 cameras connected and verified recording.', 'Customer tested and collected DVR.'],
                'expenses': [('Spare Part', 'CP Plus 12V 8CH CCTV SMPS Power Supply', Decimal('1250.00'))],
                'payments': [(Decimal('1950.00'), 'UPI', 'UPI-BALAJI-9923', 'Settled via Google Pay on delivery')],
            },
            {
                'customer': created_customers[3],
                'device_type': 'Desktop',
                'brand': 'Asus / Custom Build',
                'model': 'Intel Core i3 10th Gen Desktop',
                'serial_number': 'ASUS-H410-0981',
                'asset_number': '',
                'physical_condition': 'Cabinet side panel screw missing',
                'accessories': 'CPU Cabinet only (No cables received)',
                'complaint': 'System very slow, frequent blue screens (BSOD) and taking 10 minutes to boot.',
                'initial_diagnosis': 'Failing mechanical HDD and 100% disk usage issue.',
                'technician_notes': 'Suggest Crucial 500GB NVMe SSD upgrade + OS installation.',
                'priority': 'Medium',
                'status': 'Pending',
                'expected_completion_date': timezone.localdate() + datetime.timedelta(days=2),
                'estimated_cost': Decimal('3500.00'),
                'service_charge': Decimal('600.00'),
                'discount': Decimal('0.00'),
                'created_by': staff2,
                'updated_by': staff2,
                'progress_notes': [],
                'expenses': [],
                'payments': [],
            },
            {
                'customer': created_customers[4],
                'device_type': 'UPS',
                'brand': 'Microtek',
                'model': 'Legend 1000VA UPS',
                'serial_number': 'MTK-UPS-1000-88',
                'asset_number': 'SCH-LAB-UPS-03',
                'physical_condition': 'Good physical shape, terminals clean',
                'accessories': 'Attached Input & Output power cords',
                'complaint': 'No backup power during power cuts; turns off immediately.',
                'initial_diagnosis': '12V 7.2Ah internal battery degraded/dead.',
                'technician_notes': 'Dual battery replacement needed.',
                'priority': 'Low',
                'status': 'Completed',
                'expected_completion_date': timezone.localdate(),
                'estimated_cost': Decimal('2600.00'),
                'service_charge': Decimal('400.00'),
                'discount': Decimal('100.00'),
                'created_by': staff1,
                'updated_by': staff1,
                'completed_at': timezone.now() - datetime.timedelta(hours=2),
                'progress_notes': ['Tested with multimeter: Battery output voltage 4.2V (degraded).', 'Installed 2 fresh Exide 12V 7Ah UPS batteries and verified 30-minute backup under full load.'],
                'expenses': [('Spare Part', '2x Exide 12V 7Ah UPS Batteries', Decimal('1800.00'))],
                'payments': [(Decimal('2100.00'), 'Bank Transfer', 'NEFT-SCH-29381', 'School accounts department transfer')],
            },
            {
                'customer': created_customers[5],
                'device_type': 'Laptop',
                'brand': 'HP',
                'model': 'Pavilion Gaming 15 (Ryzen 5)',
                'serial_number': 'HP-PAV-GAM-4412',
                'asset_number': '',
                'physical_condition': 'Right hinge broken, screen bezel popping out',
                'accessories': 'HP 150W Smart Adapter, Mouse, Cooling Pad',
                'complaint': 'Right side hinge broken and thermal throttling / overheating fan noise.',
                'initial_diagnosis': 'Hinge fabrication required, thermal paste dried up.',
                'technician_notes': 'Complete body hinge structural repair and fan cleaning with Arctic MX-4 thermal paste.',
                'priority': 'High',
                'status': 'In Progress',
                'expected_completion_date': timezone.localdate() - datetime.timedelta(days=2),  # Overdue demo!
                'estimated_cost': Decimal('2800.00'),
                'service_charge': Decimal('1400.00'),
                'discount': Decimal('0.00'),
                'created_by': staff1,
                'updated_by': staff1,
                'progress_notes': ['Hinge base bracket reconstructed using reinforced industrial resin.', 'Cooling fans cleaned and old thermal pads removed.'],
                'expenses': [('Consumable', 'Arctic MX-4 High Performance Thermal Compound', Decimal('350.00'))],
                'payments': [(Decimal('1000.00'), 'Cash', '', 'Advance deposit')],
            }
        ]

        for sdata in services_data:
            progress_list = sdata.pop('progress_notes')
            expenses_list = sdata.pop('expenses')
            payments_list = sdata.pop('payments')

            svc = Service.objects.create(**sdata)
            
            # Initial history and ledger
            ServiceHistory.objects.create(
                service=svc,
                old_status='None',
                new_status=svc.status,
                changed_by=svc.created_by,
                remarks='Device inward received.'
            )
            LedgerEntry.objects.create(
                service=svc,
                action='Inward Created',
                description=f"Inward device: {svc.device_type} ({svc.brand} {svc.model}) - {svc.complaint[:80]}",
                amount=svc.estimated_cost,
                created_by=svc.created_by
            )

            # Inward Notification
            Notification.objects.create(
                service=svc,
                customer=svc.customer,
                notification_type='Inward',
                phone_number=svc.customer.phone_number,
                message=f"Dear {svc.customer.name}, your {svc.device_type} ({svc.brand} {svc.model}) has been received for service. Service ID: {svc.service_id}. ROBO DIGITAL COMPUTERS.",
                status='Sent',
                response_log='Simulated: Successful inward notification log.',
                sent_by=svc.created_by
            )

            # Progress items
            for ptext in progress_list:
                ServiceProgress.objects.create(service=svc, progress_description=ptext, created_by=svc.created_by)
                LedgerEntry.objects.create(service=svc, action='Work Progress', description=f"Update: {ptext[:100]}", created_by=svc.created_by)

            # Expenses
            for etype, edesc, eamt in expenses_list:
                Expense.objects.create(service=svc, expense_type=etype, description=edesc, amount=eamt, created_by=svc.created_by)
                LedgerEntry.objects.create(service=svc, action='Expense Added', description=f"Added {etype}: {edesc}", amount=eamt, created_by=svc.created_by)

            # Payments
            for pamt, pmethod, pref, pnotes in payments_list:
                Payment.objects.create(service=svc, amount=pamt, payment_method=pmethod, reference_number=pref, notes=pnotes, received_by=svc.created_by)
                LedgerEntry.objects.create(service=svc, action='Payment Received', description=f"Payment received ₹{pamt} via {pmethod}", amount=pamt, created_by=svc.created_by)

            # Invoices for Completed / Delivered
            if svc.status in ['Completed', 'Delivered']:
                labor = svc.service_charge if svc.service_charge > 0 else svc.estimated_cost
                parts = svc.total_expenses
                subtotal = labor + parts
                total = max(Decimal('0.00'), subtotal - svc.discount)
                paid = svc.total_paid
                balance = max(Decimal('0.00'), total - paid)

                Invoice.objects.create(
                    service=svc,
                    labor_charge=labor,
                    parts_charge=parts,
                    other_charges=Decimal('0.00'),
                    discount=svc.discount,
                    sub_total_amount=subtotal,
                    total_amount=total,
                    paid_amount=paid,
                    balance_amount=balance,
                    created_by=svc.created_by
                )
                Notification.objects.create(
                    service=svc,
                    customer=svc.customer,
                    notification_type='Completed',
                    phone_number=svc.customer.phone_number,
                    message=f"Dear {svc.customer.name}, your service {svc.service_id} is COMPLETED! Total Amount: ₹{total}, Balance: ₹{balance}. Ready for delivery. ROBO DIGITAL COMPUTERS.",
                    status='Sent',
                    response_log='Simulated: Completion notification sent.',
                    sent_by=svc.created_by
                )

        self.stdout.write(self.style.SUCCESS(f"Successfully seeded database with {len(created_customers)} customers, {len(services_data)} services, expenses, payments, and invoices!"))
