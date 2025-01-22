
STATES_CITY = {
    "":["select a state first"],
    "Andhra Pradesh": ["Amaravati", "Visakhapatnam", "Vijayawada", "Guntur", "Tirupati"],
    "Arunachal Pradesh": ["Itanagar", "Pasighat", "Tawang", "Ziro", "Bomdila"],
    "Assam": ["Guwahati", "Silchar", "Dibrugarh", "Jorhat", "Tezpur"],
    "Bihar": ["Patna", "Gaya", "Bhagalpur", "Muzaffarpur", "Darbhanga"],
    "Chhattisgarh": ["Raipur", "Bilaspur", "Durg", "Raigarh", "Korba"],
    "Goa": ["Panaji", "Vasco da Gama", "Mapusa", "Margao", "Ponda"],
    "Gujarat": ["Gandhinagar", "Ahmedabad", "Surat", "Vadodara", "Rajkot"],
    "Haryana": ["Chandigarh", "Faridabad", "Gurgaon", "Panipat", "Rohtak"],
    "Himachal Pradesh": ["Shimla", "Manali", "Dharamshala", "Solan", "Kullu"],
    "Jharkhand": ["Ranchi", "Jamshedpur", "Dhanbad", "Bokaro", "Hazaribag"],
    "Karnataka": ["Bengaluru", "Mysuru", "Mangalore", "Hubli-Dharwad", "Belgaum"],
    "Kerala": ["Thiruvananthapuram", "Kochi", "Kozhikode", "Trivandrum", "Kollam"],
    "Madhya Pradesh": ["Bhopal", "Indore", "Jabalpur", "Gwalior", "Ujjain"],
    "Maharashtra": ["Mumbai", "Pune", "Nagpur", "Nashik", "Aurangabad"],
    "Manipur": ["Imphal", "Churachandpur", "Ukhrul", "Thoubal", "Jiribam"],
    "Meghalaya": ["Shillong", "Tura", "Jowai", "Nongstoin", "Williamnagar"],
    "Mizoram": ["Aizawl", "Lunglei", "Silchar", "Champhai", "Saiha"],
    "Nagaland": ["Kohima", "Dimapur", "Mokokchung", "Wokha", "Zunheboto"],
    "Odisha": ["Bhubaneswar", "Cuttack", "Puri", "Rourkela", "Sambalpur"],
    "Punjab": ["Chandigarh", "Ludhiana", "Amritsar", "Jalandhar", "Patiala"],
    "Rajasthan": ["Jaipur", "Jodhpur", "Udaipur", "Jaisalmer", "Ajmer"],
    "Sikkim": ["Gangtok", "Pelling", "Lachung", "Yuksom", "Mangan"],
    "Tamil Nadu": ["Chennai", "Coimbatore", "Madurai", "Tiruchirappalli", "Salem"],
    "Telangana": ["Hyderabad", "Warangal", "Karimnagar", "Nizamabad", "Khammam"],
    "Tripura": ["Agartala", "Durgapur", "Udaipur", "Kailashahar", "Belonia"],
    "Uttar Pradesh": ["Lucknow", "Kanpur", "Varanasi", "Agra", "Ghaziabad"],
    "Uttarakhand": ["Dehradun", "Haridwar", "Rishikesh", "Nainital", "Mussoorie"],
    "West Bengal": ["Kolkata", "Durgapur", "Asansol", "Siliguri", "Haldia"],
    "Andaman and Nicobar Islands": ["Port Blair", "Havelock Island", "Neil Island", "Diglipur", "Mayabunder"],
    "Chandigarh": ["Chandigarh"],
    "Delhi": ["Delhi"],
    "Puducherry": ["Puducherry", "Karaikal", "Mahe", "Yanam"],
    "Ladakh": ["Leh", "Kargil", "Zanskar", "Nubra Valley", "Pangong Tso"],
    "Jammu and Kashmir": ["Srinagar", "Jammu", "Leh", "Kargil", "Anantnag"]
}

# Dummy Product Data (for rendering)
PRODUCTS = [
    {
        'id': 1,
        'name': 'Classic White Shirt',
        'price': 1999,
        'image': 'static/Products/white.jpeg',
        'description': 'A timeless classic for any wardrobe, perfect for both formal and casual occasions.',
        'details': [
            'Made from 100% premium cotton.',
            'Breathable and comfortable for all-day wear.',
            'Available in multiple sizes for the perfect fit.',
            'Machine washable and easy to maintain.',
            'Perfect for office, events, and everyday use.'
        ],
        'stock': 2,
        'category': 'Clothing',
        'brand':'Wrogn',
        'colour': 'White',
        'target_user':'Men',
        'type': 'Shirt'
    },
    {
        'id': 2,
        'name': 'Denim Jacket',
        'price': 3499,
        'image': 'static/Products/dDenim Jacket.jpeg',
        'description': 'A stylish denim jacket that adds an edgy touch to your outfit.',
        'details': [
            'Durable and soft denim fabric.',
            'Slim-fit design with button closure.',
            'Features side pockets and a classic collar.',
            'Perfect for layering in any season.',
            'Hand-wash recommended for extended durability.'
        ],
        'stock': 2,
        'category': 'Clothing',
        'brand':'Levis',
        'colour': 'Blue',
        'target_user':'Men',
        'type': 'Jacket'
    },
    {
        'id': 3,
        'name': 'Summer Floral Dress',
        'price': 2799,
        'image': 'static/Products/dSummer Floral Dress.jpeg',
        'description': 'A breezy floral dress ideal for summer outings and vacations.',
        'details': [
            'Lightweight, flowy material for comfort.',
            'Beautiful floral prints with vibrant colors.',
            'Adjustable straps for a customized fit.',
            'Perfect for brunches, picnics, or beach outings.',
            'Machine washable and fade-resistant.'
        ],
        'stock': 2,
        'category': 'Clothing',
        'brand':'Zara',
        'colour': 'orange',
        'target_user':['Women','girls'],
        'type': 'Dress'
    },
    {
        'id': 4,
        'name': 'Leather Wallet',
        'price': 1299,
        'image': 'static/Products/Leather Wallet.jpeg',
        'description': 'A sleek and functional leather wallet for everyday use.',
        'details': [
            'Crafted from genuine leather for durability.',
            'Multiple compartments for cards and cash.',
            'Compact design to fit in any pocket.',
            'Available in black and brown colors.',
            'A great gift for friends and family.'
        ],
        'stock': 2,
        'category': 'Accessories',
        'brand':'Puma',
        'colour': 'Brown',
        'target_user':'Men',
        'type': 'Wallet'
    },
    {
        'id': 5,
        'name': 'Running Shoes',
        'price': 3999,
        'image': 'static/Products/shoes.jpeg',
        'description': 'High-performance running shoes for athletes and fitness enthusiasts.',
        'details': [
            'Breathable mesh upper for ventilation.',
            'Cushioned sole for maximum comfort.',
            'Slip-resistant outsole for stability.',
            'Lightweight design for enhanced speed.',
            'Available in various sizes and colors.'
        ],
        'stock': 0,
        'category': 'Footwear',
        'brand':'Campus',
        'colour': 'Blue',
        'target_user':'Men',
        'type': 'Shoes'
    },
    # Additional 10 dummy products
    {
        'id': 6,
        'name': 'Silk Tie Set',
        'price': 999,
        'image': 'static/Products/tie.jpeg',
        'description': 'A premium silk tie set for formal occasions.',
        'details': [
            'Includes matching pocket square.',
            'Made from high-quality silk fabric.',
            'Perfect for weddings, parties, and office wear.',
            'Easy to clean and maintain.'
        ],
        'stock': 5,
        'category': 'Accessories',
        'brand':'levis',
        'colour': 'White',
        'target_user':'Men',
        'type': 'Tie'
    },
    {
        'id': 7,
        'name': 'Smartwatch',
        'price': 7999,
        'image': 'static/Products/smartwatch.jpeg',
        'description': 'A feature-packed smartwatch for health and connectivity.',
        'details': [
            'Tracks heart rate, steps, and sleep patterns.',
            'Water-resistant and durable design.',
            'Syncs with your smartphone for notifications.',
            'Available in multiple strap colors.'
        ],
        'stock': 3,
        'category': 'Electronics',
        'brand':'Apple',
        'colour': 'Black',
        'target_user':'Unisex',
        'type': 'Watch'
    },
    {
        'id': 8,
        'name': 'Backpack',
        'price': 2499,
        'image': 'static/Products/backpack.jpeg',
        'description': 'A stylish and spacious backpack for work or travel.',
        'details': [
            'Made from water-resistant material.',
            'Multiple compartments for organized storage.',
            'Comfortable shoulder straps.',
            'Available in multiple colors.'
        ],
        'stock': 4,
        'category': 'Accessories',
        'brand':'Safari',
        'colour': 'Black',
        'target_user':['Unisex'],
        'type': 'Bag'
    },
    {
        'id': 9,
        'name': 'Wireless Earbuds',
        'price': 3499,
        'image': 'static/Products/earbuds.jpeg',
        'description': 'Premium wireless earbuds with noise cancellation.',
        'details': [
            'Superior sound quality with deep bass.',
            'Long battery life for all-day use.',
            'Comes with a compact charging case.',
            'Sweat and splash resistant.'
        ],
        'stock': 6,
        'category': 'Electronics',
        'brand':'Boat',
        'colour': 'Black',
        'target_user':['Unisex'],
        'type': 'Earbuds'
    },
    {
        'id': 10,
        'name': 'Yoga Mat',
        'price': 1299,
        'image': 'static/Products/yogamat.jpeg',
        'description': 'Non-slip yoga mat for fitness and relaxation.',
        'details': [
            'Made from eco-friendly materials.',
            'Offers excellent grip and cushioning.',
            'Lightweight and easy to carry.',
            'Ideal for yoga, Pilates, and workouts.'
        ],
        'stock': 7,
        'category': 'Fitness',
        'brand':'Boldfit',
        'colour': 'Pink',
        'target_user':'Unisex',
        'type': 'Mat'
    },
    {
        'id': 11,
        'name': 'Formal Black Blazer',
        'price': 4999,
        'image': 'static/Products/blazer.jpeg',
        'description': 'A tailored blazer for formal events and office wear.',
        'details': [
            'Made from high-quality fabric.',
            'Slim-fit design with classic lapels.',
            'Available in multiple sizes.',
            'Dry clean recommended.'
        ],
        'stock': 2,
        'category': 'Clothing',
        'brand':'levis',
        'colour': 'Black',
        'target_user':['Men'],
        'type': 'Blazer'
    },
    {
        'id': 12,
        'name': 'Gaming Mouse',
        'price': 1999,
        'image': 'static/Products/gaming_mouse.jpeg',
        'description': 'Ergonomic gaming mouse with customizable buttons.',
        'details': [
            'Adjustable DPI for precision.',
            'RGB lighting for a cool aesthetic.',
            'Compatible with all major operating systems.',
            'Plug-and-play setup.'
        ],
        'stock': 8,
        'category': 'Electronics',
        'brand':'Asus',
        'colour': 'Black',
        'target_user':['Unisex'],
        'type': 'Mouse'
    },
    {
        'id': 13,
        'name': 'Cotton Bedsheet',
        'price': 1499,
        'image': 'static/Products/bedsheet.jpeg',
        'description': 'A soft and comfortable bedsheet for a good night’s sleep.',
        'details': [
            'Made from 100% cotton.',
            'Available in vibrant patterns.',
            'Machine washable and durable.',
            'Perfect for all bed sizes.'
        ],
        'stock': 10,
        'category': 'Home',
        'brand':'levis',
        'colour': 'Red',
        'target_user':'Unisex',
        'type': 'Bedsheet'
    },
    {
        'id': 14,
        'name': 'Bluetooth Speaker',
        'price': 2599,
        'image': 'static/Products/speaker.jpeg',
        'description': 'Compact Bluetooth speaker with superior sound quality.',
        'details': [
            'Long battery life and quick charging.',
            'Supports hands-free calls.',
            'Water-resistant and durable.',
            'Compatible with all Bluetooth devices.'
        ],
        'stock': 5,
        'category': 'Electronics',
        'brand': 'OnePlus',
        'colour': 'Boat',
        'colour': 'Black',
        'target_user':'Unisex',
        'type': 'Speaker'
    },
    {
        'id': 15,
        'name': 'Wrist Watch',
        'price': 3499,
        'image': 'static/Products/wristwatch.jpeg',
        'description': 'A classic wristwatch with an elegant design.',
        'details': [
            'Quartz movement for precise timekeeping.',
            'Stainless steel strap.',
            'Water-resistant up to 50 meters.',
            'Available in gold and silver tones.'
        ],
        'stock': 3,
        'category': 'Accessories',
        'brand': 'Boat',
        'colour': 'Boat',
        'colour': 'Brown',
        'target_user':['Unisex'],
        'type': 'Watch'
    }
]