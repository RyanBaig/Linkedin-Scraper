import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style
from ttkbootstrap.dialogs import Messagebox
import requests
from bs4 import BeautifulSoup
import os
from PIL import Image, ImageTk

# Store a global reference to the theme image
theme_image = None

def create_font_awesome_image(icon, size=16, color="black", theme="light"):
    """
    Creates a Font Awesome image based on the given icon, size, color, and theme.

    Parameters:
        icon (str): The name of the icon to create the image from.
        size (int): The size of the image in pixels. Default is 16.
        color (str): The color of the image. Default is "black".
        theme (str): The theme of the image. Default is "light".

    Returns:
        ImageTk.PhotoImage: The created Font Awesome image.
    """
    global theme_image  # Use the global variable
    
    theme_folder = "icons"
    if theme == "yeti":
        theme_icon_path = os.path.join(theme_folder, "light-theme.png")
    elif theme == "darkly":
        theme_icon_path = os.path.join(theme_folder, "dark-theme.png")

    # Open the PNG image with Pillow
    image = Image.open(theme_icon_path).convert("RGBA").resize((size, size))
    
    # Create a PhotoImage object and keep a reference to it
    theme_image = ImageTk.PhotoImage(image)
    return theme_image

def toggle_theme():
    """
    Toggles the theme between "yeti" and "darkly" and updates the UI accordingly.
    """
    current_theme = style.theme_use()
    new_theme = "darkly" if current_theme == "yeti" else "yeti"
    style.theme_use(new_theme)

    # Recreate the theme_image for the new theme
    theme_icon_path = os.path.join("icons", f"{new_theme}-theme.png")
    theme_image = create_font_awesome_image(theme_icon_path, size=16, theme=new_theme)

    # Update the button with the new theme_image
    theme_button.config(image=theme_image, compound=tk.LEFT)
    root.update_idletasks()

def scrape_linkedin_jobs(job_title: str):
    """
    Scrapes LinkedIn job listings based on a given job title.

    Parameters:
        job_title (str): The job title to search for.

    Returns:
        list: A list of dictionaries containing the job listings, each with the following keys:
            - title (str): The title of the job.
            - company (str): The name of the company offering the job.
    """
    search_term = job_title.lower()
    url = f"https://www.linkedin.com/jobs/search?keywords={search_term.replace(' ', '')}"

    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        job_listings = []
        job_list_ul = soup.find('ul', class_='jobs-search__results-list')
        if job_list_ul:
            for job in job_list_ul.find_all('li'):
                title_elem = job.find('h3', class_='base-search-card__title')
                company_elem = job.find('h4', class_='base-search-card__subtitle')

                if title_elem and company_elem:
                    title = title_elem.text.strip()
                    company = company_elem.text.strip()
                    job_listings.append({"title": title, "company": company})

        return job_listings
    except requests.exceptions.ConnectionError:
        return ["error"]

def show_job_listings():
    """
    Retrieves job listings based on the entered job title and displays them in the table.

    Parameters:
        None.

    Returns:
        None.
    """
    job_title = job_title_entry.get()
    if job_title:
        # Show "Searching..." message
        listbox.delete(*listbox.get_children())
        Messagebox.show_info("Searching for jobs...", "Searching...")

        job_listings = scrape_linkedin_jobs(job_title)

        if job_listings == ["error"]:
            Messagebox.show_error("Unable to connect to LinkedIn. Please check your Internet Connection and Try Again", "Network Error")

        elif job_listings:
            # Clear previous message
            listbox.delete(*listbox.get_children())

            # Populate the table with job listings
            for job in job_listings:
                listbox.insert("", tk.END, values=(job['title'], job['company']))
        else:
            # Notify the user that no jobs are found
            listbox.delete(*listbox.get_children())
            Messagebox.show_info("No jobs found for the entered job title.", "No Jobs Found.")
    else:
        # Notify the user to enter a job title
        listbox.delete(*listbox.get_children())
        Messagebox.show_error("Please enter a job title", "Missing Job Title")

root = tk.Tk()
root.title("LinkedIn Job Scraper")
root.geometry("800x600")  
root.resizable(False, False)

style = Style(theme="yeti")  # Choose a ttkbootstrap theme


# Entry for job title
job_title_label = ttk.Label(root, text="Enter Job Title:")
job_title_label.grid(row=0, column=0, padx=10, pady=10, sticky="E")

job_title_entry = ttk.Entry(root, width=30)
job_title_entry.grid(row=0, column=1, padx=5, pady=10)

# Table to display job listings
columns = ("Job Title", "Company Name")
listbox = ttk.Treeview(root, columns=columns, show="headings", height=25)
listbox.heading("Job Title", text="Job Title")
listbox.heading("Company Name", text="Company Name")
listbox.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

# Add space b/w the columns
listbox.column("Job Title", width=360, anchor=tk.W)
listbox.column("Company Name", width=400, anchor=tk.W)

# Button to refresh job listings
refresh_button = ttk.Button(root, text="Refresh Job Listings", command=show_job_listings)
refresh_button.grid(row=2, column=0, columnspan=2, pady=10)

theme_icon_path = os.path.join("icons", "light-theme.png")
theme_image = create_font_awesome_image(theme_icon_path, size=16, theme=style.theme_use())

theme_button = ttk.Button(root, text="", command=toggle_theme, image=theme_image, compound=tk.LEFT)
theme_button.grid(row=3, column=0, columnspan=2, pady=10)

root.mainloop()
