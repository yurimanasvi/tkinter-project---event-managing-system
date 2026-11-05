import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime, date

# ---------------- THEME ----------------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

BG = "#111111"
SIDEBAR = "#181818"
CARD = "#222222"
CARD2 = "#2B2B2B"
GOLD = "#D6AA60"
GOLD_HOVER = "#B98C45"
WHITE = "#F5F0E7"
MUTED = "#AAA49A"
GREEN = "#62B58A"
RED = "#D47777"

# Demo data: stored only in memory. It resets when the app closes.
events = [
    {"id": 1, "name": "TechNova Summit", "date": "2026-12-15",
     "venue": "Main Auditorium", "description": "A day of technology and innovation.",
     "budget": 45000.0},
    {"id": 2, "name": "Golden Hour Gala", "date": "2026-12-20",
     "venue": "Grand Ballroom", "description": "An evening celebration.",
     "budget": 65000.0},
    {"id": 3, "name": "Creative Minds Workshop", "date": "2027-01-08",
     "venue": "Seminar Hall 2", "description": "A hands-on creative workshop.",
     "budget": 18000.0},
]

guests = [
    {"id": 1, "name": "Aarav Sharma", "email": "aarav@example.com",
     "phone": "9876543210", "event_id": 1, "rsvp": "Confirmed", "attended": True},
    {"id": 2, "name": "Diya Patel", "email": "diya@example.com",
     "phone": "9876543211", "event_id": 2, "rsvp": "Registered", "attended": False},
    {"id": 3, "name": "Rohan Mehta", "email": "rohan@example.com",
     "phone": "9876543212", "event_id": 1, "rsvp": "Confirmed", "attended": True},
    {"id": 4, "name": "Sneha Kapoor", "email": "sneha@example.com",
     "phone": "9876543213", "event_id": 3, "rsvp": "Maybe", "attended": False},
]
next_event_id = 4
next_guest_id = 5


def button(parent, text, command, primary=False, width=110):
    return ctk.CTkButton(
        parent, text=text, command=command, width=width, height=36,
        corner_radius=9, font=ctk.CTkFont(size=12, weight="bold"),
        fg_color=GOLD if primary else CARD2,
        hover_color=GOLD_HOVER if primary else "#3A3A3A",
        text_color="#17130D" if primary else WHITE
    )


def label(parent, text, size=13, color=WHITE, bold=False):
    return ctk.CTkLabel(
        parent, text=text, text_color=color,
        font=ctk.CTkFont(size=size, weight="bold" if bold else "normal")
    )


def entry(parent, placeholder, width=250):
    return ctk.CTkEntry(
        parent, width=width, height=38, corner_radius=9,
        placeholder_text=placeholder, fg_color=CARD2,
        border_color="#454039", text_color=WHITE,
        placeholder_text_color=MUTED
    )


def clear(frame):
    for widget in frame.winfo_children():
        widget.destroy()


class Eventify(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Eventify | Event Management")
        self.geometry("1200x760")
        self.minsize(980, 640)
        self.configure(fg_color=BG)
        self.current_page = "Dashboard"

        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0, fg_color=SIDEBAR)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        self.main = ctk.CTkFrame(self, fg_color=BG, corner_radius=0)
        self.main.pack(side="right", fill="both", expand=True)

        self.build_sidebar()
        self.show_page("Dashboard")

    def build_sidebar(self):
        brand = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        brand.pack(fill="x", padx=22, pady=(30, 38))
        label(brand, "✦ EVENTIFY", 24, GOLD, True).pack(anchor="w")
        label(brand, "PLAN  •  ORGANIZE  •  CELEBRATE", 9, MUTED).pack(anchor="w", pady=(6, 0))

        self.nav = {}
        for page, symbol in [
            ("Dashboard", "⌂"), ("Events", "▦"),
            ("Guests", "♙"), ("Analytics", "▥")
        ]:
            b = ctk.CTkButton(
                self.sidebar, text=f"   {symbol}     {page}",
                command=lambda p=page: self.show_page(p),
                height=45, corner_radius=10, anchor="w",
                font=ctk.CTkFont(size=14, weight="bold"),
                fg_color="transparent", hover_color="#30291D",
                text_color=MUTED
            )
            b.pack(fill="x", padx=14, pady=5)
            self.nav[page] = b

        footer = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        footer.pack(side="bottom", fill="x", padx=22, pady=25)
        label(footer, "FRONTEND DEMO", 10, GOLD, True).pack(anchor="w")
        label(footer, "Eventify  •  Version 1.0", 10, MUTED).pack(anchor="w", pady=(6, 0))

    def show_page(self, page):
        self.current_page = page
        for name, b in self.nav.items():
            b.configure(
                fg_color=GOLD if name == page else "transparent",
                text_color="#17130D" if name == page else MUTED
            )
        clear(self.main)
        {
            "Dashboard": self.dashboard,
            "Events": self.events_page,
            "Guests": self.guests_page,
            "Analytics": self.analytics_page
        }[page]()

    def header(self, title, subtitle, add_text=None, add_command=None):
        top = ctk.CTkFrame(self.main, fg_color="transparent")
        top.pack(fill="x", padx=30, pady=(28, 20))
        left = ctk.CTkFrame(top, fg_color="transparent")
        left.pack(side="left")
        label(left, title, 27, WHITE, True).pack(anchor="w")
        label(left, subtitle, 12, MUTED).pack(anchor="w", pady=(5, 0))
        if add_text:
            button(top, add_text, add_command, True, 125).pack(side="right", pady=4)
        return top

    def stat_card(self, parent, title, value, foot):
        card = ctk.CTkFrame(parent, fg_color=CARD, corner_radius=14,
                            border_width=1, border_color="#393126")
        card.pack(side="left", fill="both", expand=True, padx=6)
        label(card, title.upper(), 10, MUTED, True).pack(anchor="w", padx=17, pady=(16, 5))
        label(card, str(value), 27, GOLD, True).pack(anchor="w", padx=17)
        label(card, foot, 10, MUTED).pack(anchor="w", padx=17, pady=(3, 15))

    def event_name(self, event_id):
        for e in events:
            if e["id"] == event_id:
                return e["name"]
        return "Unknown event"

    def dashboard(self):
        self.header("Welcome back, Admin", "Here's what's happening with your events.")
        today = date.today().isoformat()
        upcoming = [e for e in events if e["date"] >= today]
        checked = sum(g["attended"] for g in guests)
        rate = round(checked / len(guests) * 100) if guests else 0

        stats = ctk.CTkFrame(self.main, fg_color="transparent")
        stats.pack(fill="x", padx=24, pady=(0, 20))
        self.stat_card(stats, "Total events", len(events), "Events created")
        self.stat_card(stats, "Total guests", len(guests), "Registered attendees")
        self.stat_card(stats, "Upcoming", len(upcoming), "Today and future")
        self.stat_card(stats, "Attendance", f"{rate}%", "Guests checked in")

        lower = ctk.CTkFrame(self.main, fg_color="transparent")
        lower.pack(fill="both", expand=True, padx=30, pady=(0, 25))

        panel = ctk.CTkFrame(lower, fg_color=CARD, corner_radius=14)
        panel.pack(side="left", fill="both", expand=True, padx=(0, 8))
        label(panel, "UPCOMING EVENTS", 13, GOLD, True).pack(anchor="w", padx=18, pady=18)

        if not upcoming:
            label(panel, "No upcoming events. Create your first event.", 12, MUTED).pack(pady=25)
        else:
            for e in sorted(upcoming, key=lambda x: x["date"])[:6]:
                row = ctk.CTkFrame(panel, fg_color=CARD2, corner_radius=10)
                row.pack(fill="x", padx=13, pady=5)
                info = ctk.CTkFrame(row, fg_color="transparent")
                info.pack(side="left", fill="x", expand=True, padx=12, pady=10)
                label(info, e["name"], 13, WHITE, True).pack(anchor="w")
                label(info, f'{e["date"]}  •  {e["venue"]}', 10, MUTED).pack(anchor="w", pady=(4, 0))
                count = sum(g["event_id"] == e["id"] for g in guests)
                label(row, f"{count} guests", 10, GOLD, True).pack(side="right", padx=14)

        quick = ctk.CTkFrame(lower, width=230, fg_color=CARD, corner_radius=14)
        quick.pack(side="right", fill="y", padx=(8, 0))
        quick.pack_propagate(False)
        label(quick, "QUICK ACTIONS", 13, GOLD, True).pack(anchor="w", padx=18, pady=18)
        button(quick, "+  Create event", self.open_event_form, True, 190).pack(padx=18, pady=7)
        button(quick, "+  Add guest", self.open_guest_form, False, 190).pack(padx=18, pady=7)
        button(quick, "View events", lambda: self.show_page("Events"), False, 190).pack(padx=18, pady=7)
        label(quick, "ATTENDANCE RATE", 10, MUTED, True).pack(anchor="w", padx=18, pady=(35, 8))
        bar = ctk.CTkProgressBar(quick, progress_color=GOLD, fg_color=CARD2)
        bar.pack(fill="x", padx=18)
        bar.set(rate / 100)
        label(quick, f"{rate}% checked in", 11, WHITE).pack(anchor="w", padx=18, pady=8)

    # ---------------- EVENTS ----------------
    def events_page(self):
        self.header("Events", "Create, organize and manage your events.",
                    "+  Add Event", self.open_event_form)
        tools = ctk.CTkFrame(self.main, fg_color="transparent")
        tools.pack(fill="x", padx=30, pady=(0, 12))
        self.event_query = entry(tools, "Search events or venues...", 300)
        self.event_query.pack(side="left")
        button(tools, "Search", self.load_events).pack(side="left", padx=8)
        button(tools, "Show all", lambda: (self.event_query.delete(0, "end"), self.load_events())).pack(side="left")
        self.event_list = ctk.CTkScrollableFrame(self.main, fg_color="transparent")
        self.event_list.pack(fill="both", expand=True, padx=25, pady=(0, 20))
        self.load_events()

    def load_events(self):
        clear(self.event_list)
        q = self.event_query.get().lower().strip()
        matches = [e for e in events if q in e["name"].lower() or q in e["venue"].lower()]
        if not matches:
            label(self.event_list, "No events found.", 13, MUTED).pack(pady=35)
            return
        for e in matches:
            card = ctk.CTkFrame(self.event_list, fg_color=CARD, corner_radius=13,
                                border_width=1, border_color="#393126")
            card.pack(fill="x", padx=5, pady=7)
            stripe = ctk.CTkFrame(card, fg_color=GOLD, width=5, corner_radius=3)
            stripe.pack(side="left", fill="y", padx=(0, 14), pady=12)
            info = ctk.CTkFrame(card, fg_color="transparent")
            info.pack(side="left", fill="x", expand=True, pady=13)
            label(info, e["name"], 16, WHITE, True).pack(anchor="w")
            label(info, f'{e["date"]}   •   {e["venue"]}', 11, MUTED).pack(anchor="w", pady=4)
            if e["description"]:
                label(info, e["description"], 10, MUTED).pack(anchor="w")
            count = sum(g["event_id"] == e["id"] for g in guests)
            label(info, f'{count} guests   •   Budget: ₹{e["budget"]:,.0f}', 10, GOLD).pack(anchor="w", pady=(5, 0))
            actions = ctk.CTkFrame(card, fg_color="transparent")
            actions.pack(side="right", padx=14)
            button(actions, "Edit", lambda item=e: self.open_event_form(item), False, 65).pack(pady=4)
            button(actions, "Delete", lambda item=e: self.delete_event(item["id"]), False, 65).pack(pady=4)

    def open_event_form(self, event=None):
        global next_event_id
        win = ctk.CTkToplevel(self)
        win.title("Event details")
        win.geometry("460x555")
        win.resizable(False, False)
        win.configure(fg_color=BG)
        win.transient(self)
        win.grab_set()
        label(win, "EDIT EVENT" if event else "CREATE AN EVENT", 21, GOLD, True).pack(anchor="w", padx=28, pady=(24, 5))
        label(win, "Fill in the details below.", 11, MUTED).pack(anchor="w", padx=28, pady=(0, 15))

        fields = {}
        specs = [
            ("Name", "Event name"),
            ("Date", "YYYY-MM-DD"),
            ("Venue", "Event venue"),
            ("Description", "Short description"),
            ("Budget", "Budget in ₹")
        ]
        for key, hint in specs:
            label(win, key, 11, MUTED, True).pack(anchor="w", padx=30, pady=(7, 4))
            fields[key] = entry(win, hint, 395)
            fields[key].pack(padx=30)
        if event:
            vals = [event["name"], event["date"], event["venue"], event["description"], str(event["budget"])]
            for (key, _), val in zip(specs, vals):
                fields[key].insert(0, val)

        def save():
            global next_event_id
            name = fields["Name"].get().strip()
            d = fields["Date"].get().strip()
            venue = fields["Venue"].get().strip()
            try:
                datetime.strptime(d, "%Y-%m-%d")
                budget = float(fields["Budget"].get() or 0)
                if budget < 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Invalid details", "Use a valid date (YYYY-MM-DD) and a non-negative budget.", parent=win)
                return
            if not name or not venue:
                messagebox.showwarning("Missing details", "Event name and venue are required.", parent=win)
                return
            if event:
                event.update(name=name, date=d, venue=venue,
                             description=fields["Description"].get().strip(), budget=budget)
            else:
                events.append({"id": next_event_id, "name": name, "date": d,
                               "venue": venue, "description": fields["Description"].get().strip(),
                               "budget": budget})
                next_event_id += 1
            win.destroy()
            self.refresh()

        button(win, "Save Event", save, True, 395).pack(padx=30, pady=20)

    def delete_event(self, event_id):
        if messagebox.askyesno("Delete event", "Delete this event and its guest registrations?"):
            events[:] = [e for e in events if e["id"] != event_id]
            guests[:] = [g for g in guests if g["event_id"] != event_id]
            self.refresh()

    # ---------------- GUESTS ----------------
    def guests_page(self):
        self.header("Guests", "Manage registrations, RSVP and attendance.",
                    "+  Add Guest", self.open_guest_form)
        tools = ctk.CTkFrame(self.main, fg_color="transparent")
        tools.pack(fill="x", padx=30, pady=(0, 12))
        self.guest_query = entry(tools, "Search guests or events...", 300)
        self.guest_query.pack(side="left")
        button(tools, "Search", self.load_guests).pack(side="left", padx=8)
        button(tools, "Show all", lambda: (self.guest_query.delete(0, "end"), self.load_guests())).pack(side="left")

        self.guest_list = ctk.CTkScrollableFrame(self.main, fg_color="transparent")
        self.guest_list.pack(fill="both", expand=True, padx=25, pady=(0, 10))
        self.load_guests()

    def load_guests(self):
        clear(self.guest_list)
        q = self.guest_query.get().lower().strip()
        matches = [g for g in guests if q in g["name"].lower()
                   or q in g["email"].lower() or q in self.event_name(g["event_id"]).lower()]
        if not matches:
            label(self.guest_list, "No guests found.", 13, MUTED).pack(pady=35)
            return
        for g in matches:
            card = ctk.CTkFrame(self.guest_list, fg_color=CARD, corner_radius=12)
            card.pack(fill="x", padx=5, pady=6)
            info = ctk.CTkFrame(card, fg_color="transparent")
            info.pack(side="left", fill="x", expand=True, padx=15, pady=12)
            label(info, g["name"], 14, WHITE, True).pack(anchor="w")
            label(info, f'{g["email"]}   •   {g["phone"]}', 10, MUTED).pack(anchor="w", pady=3)
            label(info, f'{self.event_name(g["event_id"])}   •   {g["rsvp"]}', 10, GOLD).pack(anchor="w")
            status = "CHECKED IN" if g["attended"] else "NOT CHECKED IN"
            label(card, status, 10, GREEN if g["attended"] else MUTED, True).pack(side="left", padx=12)
            actions = ctk.CTkFrame(card, fg_color="transparent")
            actions.pack(side="right", padx=12)
            button(actions, "Check in", lambda item=g: self.check_in(item), True, 85).pack(pady=3)
            button(actions, "Delete", lambda item=g: self.delete_guest(item), False, 65).pack(pady=3)

    def open_guest_form(self):
        global next_guest_id
        if not events:
            messagebox.showinfo("No events", "Create an event before adding guests.")
            return
        win = ctk.CTkToplevel(self)
        win.title("Register guest")
        win.geometry("440x480")
        win.resizable(False, False)
        win.configure(fg_color=BG)
        win.transient(self)
        win.grab_set()
        label(win, "REGISTER A GUEST", 21, GOLD, True).pack(anchor="w", padx=28, pady=(25, 5))
        label(win, "Add attendee details and choose an event.", 11, MUTED).pack(anchor="w", padx=28, pady=(0, 15))

        fields = {}
        for key, hint in [("Name", "Full name"), ("Email", "Email address"), ("Phone", "Phone number")]:
            label(win, key, 11, MUTED, True).pack(anchor="w", padx=30, pady=(8, 4))
            fields[key] = entry(win, hint, 380)
            fields[key].pack(padx=30)

        label(win, "Event", 11, MUTED, True).pack(anchor="w", padx=30, pady=(13, 4))
        choices = {f'{e["name"]}  ({e["date"]})': e["id"] for e in events}
        event_choice = ctk.CTkOptionMenu(win, values=list(choices.keys()), width=380,
                                         fg_color=CARD2, button_color=GOLD,
                                         button_hover_color=GOLD_HOVER)
        event_choice.pack(padx=30)

        label(win, "RSVP status", 11, MUTED, True).pack(anchor="w", padx=30, pady=(12, 4))
        rsvp = ctk.CTkOptionMenu(win, values=["Registered", "Confirmed", "Maybe", "Cancelled"],
                                 width=380, fg_color=CARD2, button_color=GOLD,
                                 button_hover_color=GOLD_HOVER)
        rsvp.pack(padx=30)

        def save():
            global next_guest_id
            name = fields["Name"].get().strip()
            if not name:
                messagebox.showwarning("Missing name", "Guest name is required.", parent=win)
                return
            guests.append({
                "id": next_guest_id, "name": name,
                "email": fields["Email"].get().strip(),
                "phone": fields["Phone"].get().strip(),
                "event_id": choices[event_choice.get()],
                "rsvp": rsvp.get(), "attended": False
            })
            next_guest_id += 1
            win.destroy()
            self.refresh()

        button(win, "Register Guest", save, True, 380).pack(padx=30, pady=20)

    def check_in(self, guest):
        guest["attended"] = True
        self.load_guests()

    def delete_guest(self, guest):
        if messagebox.askyesno("Delete guest", f'Remove {guest["name"]} from the guest list?'):
            guests.remove(guest)
            self.load_guests()

    # ---------------- ANALYTICS ----------------
    def analytics_page(self):
        self.header("Analytics", "A snapshot of event registrations and attendance.")
        total = len(guests)
        attended = sum(g["attended"] for g in guests)
        confirmed = sum(g["rsvp"] == "Confirmed" for g in guests)
        budget = sum(e["budget"] for e in events)
        rate = round(attended / total * 100) if total else 0

        stats = ctk.CTkFrame(self.main, fg_color="transparent")
        stats.pack(fill="x", padx=24, pady=(0, 20))
        self.stat_card(stats, "Events created", len(events), "All events")
        self.stat_card(stats, "Registered guests", total, "Across all events")
        self.stat_card(stats, "Confirmed RSVPs", confirmed, "Confirmed attendees")
        self.stat_card(stats, "Total budget", f"₹{budget:,.0f}", "Combined event budgets")

        attendance = ctk.CTkFrame(self.main, fg_color=CARD, corner_radius=14)
        attendance.pack(fill="x", padx=30, pady=(0, 14))
        label(attendance, "ATTENDANCE OVERVIEW", 13, GOLD, True).pack(anchor="w", padx=20, pady=(18, 8))
        label(attendance, f"{attended} of {total} guests checked in  •  {rate}%", 13, WHITE).pack(anchor="w", padx=20, pady=(0, 12))
        bar = ctk.CTkProgressBar(attendance, progress_color=GOLD, fg_color=CARD2, height=13)
        bar.pack(fill="x", padx=20, pady=(0, 20))
        bar.set(rate / 100)

        breakdown = ctk.CTkFrame(self.main, fg_color=CARD, corner_radius=14)
        breakdown.pack(fill="both", expand=True, padx=30, pady=(0, 25))
        label(breakdown, "EVENT BUDGET BREAKDOWN", 13, GOLD, True).pack(anchor="w", padx=20, pady=18)
        if not events:
            label(breakdown, "Create events to see budget insights.", 12, MUTED).pack(anchor="w", padx=20)
        for e in events:
            row = ctk.CTkFrame(breakdown, fg_color="transparent")
            row.pack(fill="x", padx=20, pady=7)
            label(row, e["name"], 12, WHITE, True).pack(side="left")
            label(row, f'₹{e["budget"]:,.2f}', 12, GOLD).pack(side="right")

    def refresh(self):
        self.show_page(self.current_page)


if __name__ == "__main__":
    app = Eventify()
    app.mainloop()
