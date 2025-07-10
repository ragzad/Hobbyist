# Hobbyist: Project & Inventory Management App

**Hobbyist** is a full-stack web application designed to provide makers, crafters, and hobbyists with a powerful and intuitive platform to manage their projects from concept to completion. It offers integrated tools for project planning, task management, inventory tracking, and cost calculation, all within a clean and responsive user interface.

- **Live Deployed Application:** [Link to live site]
- **GitHub Repository:** [https://github.com/ragzad/Hobbyist]

---

## Table of Contents

1.  [Project Rationale & Purpose](#project-rationale--purpose)
    -   [Target Audience](#target-audience)
    -   [User Stories](#user-stories)
2.  [UX Design Rationale](#ux-design-rationale)
    -   [Information Hierarchy](#information-hierarchy)
    -   [User Control & Interaction](#user-control--interaction)
    -   [Consistency & Feedback](#consistency--feedback)
    -   [Wireframes](#wireframes)
3.  [Key Features](#key-features)
4.  [Technology Stack](#technology-stack)
    -   [Backend](#backend)
    -   [Frontend](#frontend)
    -   [Database](#database)
    -   [Deployment](#deployment)
5.  [Data Schema](#data-schema)
    -   [Database ERD](#database-erd)
    -   [Model Descriptions](#model-descriptions)
6.  [Setup & Installation](#setup--installation)
7.  [Running the Application](#running-the-application)
    -   [Running Locally](#running-locally)
    -   [Environment Variables](#environment-variables)
8.  [Testing Procedures](#testing-procedures)
9.  [Deployment Guide](#deployment-guide)
10. [Credits & Attributions](#credits--attributions)

---

## Project Rationale & Purpose

Creative projects often involve numerous moving parts: ideas, tasks, materials, and costs. Keeping track of these elements can be chaotic, relying on scattered notebooks, spreadsheets, and disconnected apps. This disorganization can stifle creativity, lead to budget overruns, and make it difficult to replicate past successes.

**Hobbyist** was created to solve this problem by providing a single, centralized hub for all project-related information. It empowers users to bring structure to their creative process, allowing them to focus on what they do best: creating.

### Target Audience

The application is designed for:

* **DIY Enthusiasts:** Woodworkers, electronics tinkerers, and home improvement warriors.
* **Crafters & Artisans:** Knitters, painters, jewelers, and model makers.
* **Makers & Inventors:** Anyone building physical or digital products in a workshop or home lab.

### User Stories

* As a **new user**, I want to sign up for an account easily so I can start organizing my projects.
* As a **logged-in user**, I want to create a new project, giving it a name, description, and cover image.
* As a **project manager**, I want to add specific, actionable tasks to my projects to create a clear plan.
* As an **organizer**, I want to sort my projects and tasks to prioritize my work effectively.
* As a **budget-conscious maker**, I want to add items to a central inventory, track their costs, and assign them to projects to understand my total expenses.
* As a **premium user**, I want to upgrade my account via a secure payment system to unlock advanced features.

---

## UX Design Rationale

The user experience is designed to be intuitive, efficient, and encouraging, adhering to core UX principles.

### Information Hierarchy

* **Semantic HTML:** The application uses semantic HTML5 tags (`<nav>`, `<main>`, `<header>`, `<section>`) to create a logical document structure, which is crucial for accessibility and SEO.
* **Visual Priority:** Key information, such as project titles and task descriptions, is given prominence. Interactive elements like buttons and links are clearly styled and easily identifiable. The dashboard (Project List) provides an immediate, high-level overview of all ongoing work.
* **Intuitive Navigation:** A persistent navigation bar provides access to core sections (Projects, Inventory, Profile) from anywhere in the app. The flow is logical: users start with a list of projects and can drill down into the details of a specific project, its tasks, and its associated inventory.

### User Control & Interaction

* **User-Initiated Actions:** The application avoids disruptive elements like pop-ups or auto-playing media. All actions, including creating, editing, and deleting data, are initiated by the user.
* **Forgiving Design:** Destructive actions, such as deleting a project or task, require an explicit confirmation step, preventing accidental data loss.
* **No Dead Ends:** All pages are linked logically. In the event of a 404 error, the user is presented with a clean error page with a clear link back to the main dashboard.

### Consistency & Feedback

* **Visual Consistency:** A consistent design language (colors, fonts, spacing, button styles) is used across all pages, ensuring a predictable and learnable interface.
* **Immediate Feedback:** The interface, powered by **HTMX**, provides instant feedback for user actions. When a task is added, a project is updated, or an item is deleted, the UI updates immediately without a full page reload, confirming the action was successful.
* **Clear Messaging:** The Django messaging framework is used to display clear success or error messages at the top of the page after significant actions (e.g., "Project created successfully!").

### Wireframes

*(In a real-world scenario, you would include images of your wireframes here to visually represent the UI/UX planning process.)*

---

## Key Features

* **Full CRUD Functionality:** Create, Read, Update, and Delete operations for Projects, Tasks, and Inventory Items.
* **User Authentication:** Secure user registration, login, and logout functionality. User-specific data access ensures privacy.
* **Project & Task Management:** Create projects and add associated tasks. Tasks can be reordered via drag-and-drop.
* **Inventory & Cost Tracking:** Manage a central inventory of materials. Assign inventory items to projects to automatically calculate total project costs.
* **Subscription Payments:** Integration with **Stripe** for secure processing of subscription payments, including a webhook for automatic fulfillment.
* **Interactive Frontend:** A dynamic user interface built with **HTMX** that allows for partial page updates, providing a smooth, app-like experience without complex JavaScript frameworks.

---

## Technology Stack

### Backend

* **Framework:** Django
* **Language:** Python
* **E-commerce:** Stripe API
* **Web Server Gateway:** Gunicorn

### Frontend

* **Styling:** Bootstrap 5
* **Interactivity:** HTMX
* **UI Libraries:** Sortable.js (for drag-and-drop)

### Database

* **Development:** SQLite3
* **Production:** PostgreSQL

### Deployment

* **Platform:** Heroku (or any similar PaaS)
* **Static Files:** WhiteNoise

---

## Data Schema

The application uses a relational database to store data across three primary apps: `users`, `projects`, and `payments`.

### Database ERD

*(In a real-world scenario, an image of the Entity-Relationship Diagram would be embedded here.)*

### Model Descriptions

#### `users` App

* `User` (Django's built-in model)
    * Stores standard user authentication details (username, password, email).
* `Profile`
    * **One-to-One with `User`:** Extends the user model.
    * `is_pro`: BooleanField. Tracks if the user has an active premium subscription. Defaults to `False`.
    * `stripe_customer_id`: CharField. Stores the unique customer ID from Stripe for managing subscriptions.

#### `projects` App

* `Folder`
    * `name`: CharField. The name of the folder.
    * `user`: ForeignKey to `User`. Each folder belongs to a specific user.
* `Project`
    * `user`: ForeignKey to `User`. The user who owns the project.
    * `folder`: ForeignKey to `Folder`. The folder this project is organized into (optional).
    * `title`, `description`, `cover_image`, `is_public`, `status`.
    * **Method `get_total_cost()`:** Calculates and returns the total cost of all `InventoryItem`s associated with this project.
* `Task`
    * `project`: ForeignKey to `Project`. Each task is part of a single project.
    * `title`, `notes`, `image`, `completed`, `order`.
* `InventoryItem`
    * `user`: ForeignKey to `User`. The user who owns the inventory item.
    * `project`: ManyToManyField to `Project`. A single inventory item can be used in multiple projects.
    * `folder`: ForeignKey to `Folder`. The folder this item is organized into (optional).
    * `name`, `quantity`, `cost`.

#### `payments` App

* `StripeEvent`
    * Stores a record of incoming webhook events from Stripe to prevent duplicate processing.
    * `stripe_event_id`: CharField. The unique ID of the event from Stripe.

---

## Setup & Installation

To run this project locally, follow these steps.

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/your-username/hobbyist.git](https://github.com/your-username/hobbyist.git)
    cd hobbyist/core
    ```

2.  **Create a Virtual Environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set Up Environment Variables:**
    -   Create a file named `.env` in the `core/` directory.
    -   Add the required variables (see [Environment Variables](#environment-variables) section below).

5.  **Apply Database Migrations:**
    ```bash
    python manage.py migrate
    ```

6.  **Create a Superuser:**
    ```bash
    python manage.py createsuperuser
    ```

---

## Running the Application

### Running Locally

Once the setup is complete, you can start the development server:

```bash
python manage.py runserver