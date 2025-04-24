# QuickEats

An intermediate level food delivery application, with visually appealing interface, having services food delivery, parcel delivery etc

## 📜 Overview

**QuickEats** is a user-friendly food delivery application designed to provide services like food ordering and parcel delivery. The application is built with Python and leverages the following technologies:

- **Tkinter**: Provides the graphical user interface of applicationn.
- **ttkbootstrap**: Modern version of Tkinter, that enhances the visual appeal of the application with modern, stylish components.
- **Matplotlib**: Used for creating and displaying graph to visualize revenue distribution analytics.

## 📂 Project Structure
```bash
QuickEats/
│
├── app.py
├── database.py
├── graph_plot.py
├── data/
│   ├── records.json
│   ├── delivery_records.json
│   ├── menu.json
│   └── accounts.json
├── fonts.md
└── requirements.txt
```
### Files Overview

- **app.py**:
  - **Authentication**: Manages user login and registration.
  - **Home Dashboard**: Central hub for accessing various features.
    - **Profile Management**: Update and manage your profile information (name, email, password, address).
    - **Services**: 
      - **Food Ordering**: Browse and order from a dynamic menu.
      - **Parcel Delivery**: Simplified parcel sending process.
    - **Analytics**: Visualize revenue distribution per item.
    - **Feedback**: Direct link to an online Form for providing feedback.
    - **Account Deletion**: Permanently remove your account.

- **database.py**:
  - Encapsulates all data handling logic.
  - Facilitates data addition and retrieval with JSON files, which store application data.

- **data/**:
  - **records.json**: Stores detailed order records.
  - **delivery_record.json**: Logs parcel delivery records.
  - **menu.json**: Holds data for the food menu.
  - **accounts.json**: Contains user account details.

## 🚀 Getting Started

### Installation

Follow these steps to set up the project on your local machine:

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/ahmadrazacdx/QuickEats.git
    cd QuickEats
    ```
2. **Install Dependencies**:
    Ensure Python is installed, then run:
    ```bash
    pip install -r requirements.txt
    ```
3. **Run the Application**:
    ```bash
    python app.py
    ```

### Prerequisites

- **Python 3.10 or above** installed on your system.
- **Fonts** mentioned in fonts.md must be installed on your system for better user experience.
- **Internet connection** to access the Google Form for feedback.

## 🎯 Key Features

- **🔒 Secure User Authentication**: Reliable login and registration system to keep user data safe.
- **👤 Profile Management**: Easily update personal information, including name, email, password, and address.
- **🍽️ Food Ordering**: Browse a dynamic menu and place your food orders.
- **📦 Parcel Delivery**: A user-friendly interface for sending parcels in simpler steps.
- **📊 Analytics**: Gain insights with revenue distribution graph.
- **📝 Feedback**: Provide feedback directly via a Microsoft Form.
- **🗑️ Account Deletion**: Option for users to permanently delete their accounts.
- **⚠ Exception Handling**: All the potential exceptions and errors handled seamlessly.

## 📊 Data Management

QuickEats uses **JSON** files as a lightweight, efficient means of data storage:

- **records.json**: Captures and stores all order details.
- **delivery_record.json**: Logs every parcel delivery transaction.
- **menu.json**: Contains up-to-date menu information.
- **accounts.json**: Manages user accounts and profile information.



