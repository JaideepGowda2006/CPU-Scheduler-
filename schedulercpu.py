# === Step 1: Import necessary libraries ===
# 'customtkinter' is the library we use to create the modern graphical user interface (GUI).
import customtkinter as ctk
# 'time' is used to create artificial delays (time.sleep) to simulate the CPU working.
import time
# 'collections.deque' is Python's specialized and highly efficient implementation of a Queue.
from collections import deque

# === Step 2: Define the Main GUI Application ===
# We create a class that inherits from CustomTkinter's 'CTk' class. This makes our class the main application window.
class SchedulerApp(ctk.CTk):
    # The __init__ method is the constructor. It runs automatically when the App is created and sets up the entire program.
    def __init__(self):
        super().__init__()
        self.title("CPU Scheduler Simulation (FIFO Queue)")
        self.geometry("800x400")

        # --- The Core Data Structure: A Queue ---
        # We declare our queue here. 'deque' is chosen because it provides very fast, O(1) time complexity
        # for adding to the end and removing from the front, which is perfect for a queue.
        #
        # In this implementation:
        # - Adding to the queue (ENQUEUE) is done with the .append() method.
        # - Removing from the queue (DEQUEUE) is done with the .popleft() method.
        self.process_queue = deque()
        
        # A simple counter to give each new process a unique name (P1, P2, etc.).
        self.process_counter = 0

        # --- GUI Section 1: The Control Buttons ---
        # A Frame is a container to help organize other widgets.
        control_frame = ctk.CTkFrame(self)
        control_frame.pack(pady=10, fill="x", padx=10)

        # The 'Add New Process' button. The 'command' parameter links this button's click event
        # to our 'add_process' function. This is the user's trigger for the ENQUEUE operation.
        self.add_button = ctk.CTkButton(control_frame, text="Add New Process", command=self.add_process)
        self.add_button.pack(side="left", padx=10, pady=10)

        # The 'Start Simulation' button. Its click event is linked to the 'start_simulation' function.
        self.start_button = ctk.CTkButton(control_frame, text="Start Simulation", command=self.start_simulation)
        self.start_button.pack(side="left", padx=10, pady=10)

        # --- GUI Section 2: The Visualization Area ---
        # This frame will contain the visual representations of the CPU and the Ready Queue.
        vis_frame = ctk.CTkFrame(self)
        vis_frame.pack(pady=10, padx=10, fill="both", expand=True)
        vis_frame.grid_columnconfigure(1, weight=1) # This allows the queue frame to stretch horizontally.

        # The "CPU" visual area.
        ctk.CTkLabel(vis_frame, text="CPU", font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, padx=10)
        self.cpu_frame = ctk.CTkFrame(vis_frame, fg_color="gray20", height=80, width=100)
        self.cpu_frame.grid(row=1, column=0, padx=10, pady=10)
        self.cpu_label = ctk.CTkLabel(self.cpu_frame, text="", font=ctk.CTkFont(size=20, weight="bold"))
        self.cpu_label.place(relx=0.5, rely=0.5, anchor="center") # .place() centers the text inside the frame.

        # The "Ready Queue" visual area, which will show the state of our queue data structure.
        ctk.CTkLabel(vis_frame, text="Ready Queue (FIFO)", font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=1, padx=10)
        self.queue_frame = ctk.CTkFrame(vis_frame, fg_color="gray20", height=80)
        self.queue_frame.grid(row=1, column=1, padx=10, pady=10, sticky="ew") # 'sticky="ew"' makes it stretch East-West.

        # This is a helper list. It does NOT store the processes themselves,
        # but it keeps track of the GUI label widgets we create so we can easily delete them later when we refresh the display.
        self.queue_labels = []

    def add_process(self):
        """
        This function handles the ENQUEUE operation. It's called when the user clicks 'Add New Process'.
        It adds a new item to the END of the process_queue.
        """
        self.process_counter += 1
        process_name = f"P{self.process_counter}"
        
        # --- THIS IS THE ENQUEUE OPERATION ---
        # We use .append() to add the new process to the right side (the end) of our deque.
        self.process_queue.append(process_name)
        
        # Print to the console for our own debugging to confirm the state of the queue.
        print(f"ENQUEUE: Added {process_name}. Queue is now: {list(self.process_queue)}")
        
        # After modifying the data structure, we must update the GUI to reflect the change.
        self.update_queue_display()

    def update_queue_display(self):
        """
        This function is purely for the GUI. It redraws the visual representation of the queue.
        It reads the current state of the 'process_queue' deque and creates a label for each item.
        """
        # First, destroy all the old labels to clear the display.
        for label in self.queue_labels:
            label.destroy()
        self.queue_labels.clear()

        # Then, create new labels for each process currently in our queue data structure.
        for i, process_name in enumerate(self.process_queue):
            proc_label = ctk.CTkLabel(self.queue_frame, text=process_name, 
                                      fg_color="dodgerblue", corner_radius=5,
                                      font=ctk.CTkFont(size=18, weight="bold"))
            # We use .place() to position them side-by-side to visually look like a queue.
            proc_label.place(x=10 + i * 80, y=25)
            self.queue_labels.append(proc_label)

    def start_simulation(self):
        """
        This function is called when the 'Start Simulation' button is clicked.
        It disables the buttons and begins the process of dequeuing items.
        """
        # Disable buttons to prevent the user from adding new processes while the simulation is running.
        self.add_button.configure(state="disabled")
        self.start_button.configure(state="disabled")

        # Call the function that will process the first item from the queue.
        self.process_next_item()

    def process_next_item(self):
        """
        This function handles the DEQUEUE operation. It takes one item from the front of the queue
        and "processes" it. It then schedules itself to run again to process the next item.
        """
        # We only proceed if our queue data structure is not empty.
        if self.process_queue:
            # --- THIS IS THE DEQUEUE OPERATION ---
            # We use .popleft() to remove the process from the left side (the front) of our deque.
            # This is the essence of the First-In, First-Out (FIFO) principle.
            current_process = self.process_queue.popleft()
            
            # Print to the console for our own debugging.
            print(f"DEQUEUE: Processing {current_process}. Queue is now: {list(self.process_queue)}")

            # --- Visualization Steps ---
            self.update_queue_display() # Update the queue display to show that the item has left.
            self.cpu_label.configure(text=current_process, fg_color="limegreen") # Show the current process in the "CPU".
            self.update() # Force the GUI to redraw immediately.

            # This simulates the CPU doing work. We pause the program for 2 seconds.
            time.sleep(2)

            # Clear the CPU display to show the process is finished.
            self.cpu_label.configure(text="", fg_color="transparent")
            self.update()
            
            # This is how we create an animation loop in a GUI.
            # Instead of a 'while' loop that would freeze the window, we tell the app to call this function again
            # after a 500ms delay. This keeps the GUI responsive.
            self.after(500, self.process_next_item)
        else:
            # If the queue is empty, the simulation is over.
            print("Simulation Finished: Queue is empty.")
            # Re-enable the buttons so the user can run another simulation.
            self.add_button.configure(state="normal")
            self.start_button.configure(state="normal")

# --- Step 3: Start the Application ---
# This is a standard Python entry point. The code inside this 'if' block only runs
# when the script is executed directly.
if __name__ == "__main__":
    # We create an instance of our SchedulerApp class. This calls the __init__ method and builds the window.
    app = SchedulerApp()
    # app.mainloop() starts the GUI's event loop. The application will now wait for user actions (like button clicks)
    # and respond to them. It will stay running until the user closes the window.
    app.mainloop()

