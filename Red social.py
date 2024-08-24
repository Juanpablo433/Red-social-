import tkinter as tk
from tkinter import scrolledtext, simpledialog, messagebox

class SocialNetworkApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Red Social")

        self.users = {
            'admin': {'password': 'password', 'friends': [], 'posts': []}
        }
        self.current_user = None

        self.create_login_frame()

    def create_login_frame(self):
        self.login_frame = tk.Frame(self.root)
        self.login_frame.pack(padx=10, pady=10)

        self.username_label = tk.Label(self.login_frame, text="Nombre de Usuario")
        self.username_label.pack()

        self.username_entry = tk.Entry(self.login_frame)
        self.username_entry.pack(pady=5)

        self.password_label = tk.Label(self.login_frame, text="Contraseña")
        self.password_label.pack()

        self.password_entry = tk.Entry(self.login_frame, show='*')
        self.password_entry.pack(pady=5)

        self.login_button = tk.Button(self.login_frame, text="Iniciar Sesión", command=self.login)
        self.login_button.pack(pady=5)

        self.register_button = tk.Button(self.login_frame, text="Registrar", command=self.register)
        self.register_button.pack()

    def create_main_frame(self):
        self.login_frame.pack_forget()

        # Crear el área de publicaciones
        self.post_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=50, height=10, state=tk.DISABLED)
        self.post_area.pack(padx=10, pady=10)

        # Crear el campo para ingresar nuevas publicaciones
        self.new_post_frame = tk.Frame(self.root)
        self.new_post_frame.pack(padx=10, pady=10)

        self.new_post_entry = tk.Entry(self.new_post_frame, width=40)
        self.new_post_entry.pack(side=tk.LEFT, padx=(0, 10))

        self.add_post_button = tk.Button(self.new_post_frame, text="Agregar Publicación", command=self.add_post)
        self.add_post_button.pack(side=tk.LEFT)

        # Crear el área de perfil
        self.profile_frame = tk.Frame(self.root)
        self.profile_frame.pack(padx=10, pady=10)

        self.profile_label = tk.Label(self.profile_frame, text="Perfil del Usuario", font=("Arial", 14))
        self.profile_label.pack()

        self.profile_text = tk.Label(self.profile_frame, text="Nombre: Usuario\nBio: Aquí va la biografía del usuario.", justify=tk.LEFT)
        self.profile_text.pack(pady=5)

        self.view_profile_button = tk.Button(self.profile_frame, text="Ver Perfil", command=self.view_profile)
        self.view_profile_button.pack()

        # Crear el área de mensajes
        self.messages_frame = tk.Frame(self.root)
        self.messages_frame.pack(padx=10, pady=10)

        self.messages_area = scrolledtext.ScrolledText(self.messages_frame, wrap=tk.WORD, width=50, height=10, state=tk.DISABLED)
        self.messages_area.pack()

        self.new_message_entry = tk.Entry(self.messages_frame, width=40)
        self.new_message_entry.pack(side=tk.LEFT, padx=(0, 10))

        self.send_message_button = tk.Button(self.messages_frame, text="Enviar Mensaje", command=self.send_message)
        self.send_message_button.pack(side=tk.LEFT)

        # Crear la lista de usuarios
        self.users_list_frame = tk.Frame(self.root)
        self.users_list_frame.pack(padx=10, pady=10)

        self.users_list_label = tk.Label(self.users_list_frame, text="Usuarios", font=("Arial", 14))
        self.users_list_label.pack()

        self.users_listbox = tk.Listbox(self.users_list_frame, height=10, width=20)
        self.users_listbox.pack()
        self.update_users_list()

        # Crear el área de notificaciones
        self.notifications_frame = tk.Frame(self.root)
        self.notifications_frame.pack(padx=10, pady=10)

        self.notifications_area = scrolledtext.ScrolledText(self.notifications_frame, wrap=tk.WORD, width=50, height=10, state=tk.DISABLED)
        self.notifications_area.pack()

        self.add_notification("Bienvenido a la red social!")

        # Agregar funcionalidad de amigos y comentarios
        self.create_friend_and_comment_section()

    def create_friend_and_comment_section(self):
        # Área de amigos
        self.friends_frame = tk.Frame(self.root)
        self.friends_frame.pack(padx=10, pady=10)

        self.friends_label = tk.Label(self.friends_frame, text="Amigos", font=("Arial", 14))
        self.friends_label.pack()

        self.friends_listbox = tk.Listbox(self.friends_frame, height=10, width=20)
        self.friends_listbox.pack()

        self.add_friend_entry = tk.Entry(self.friends_frame, width=20)
        self.add_friend_entry.pack(side=tk.LEFT, padx=(0, 10))

        self.add_friend_button = tk.Button(self.friends_frame, text="Agregar Amigo", command=self.add_friend)
        self.add_friend_button.pack(side=tk.LEFT)

        # Área de comentarios
        self.comments_frame = tk.Frame(self.root)
        self.comments_frame.pack(padx=10, pady=10)

        self.comments_label = tk.Label(self.comments_frame, text="Comentarios en la Publicación", font=("Arial", 14))
        self.comments_label.pack()

        self.comments_area = scrolledtext.ScrolledText(self.comments_frame, wrap=tk.WORD, width=50, height=10, state=tk.DISABLED)
        self.comments_area.pack()

        self.new_comment_entry = tk.Entry(self.comments_frame, width=40)
        self.new_comment_entry.pack(side=tk.LEFT, padx=(0, 10))

        self.add_comment_button = tk.Button(self.comments_frame, text="Agregar Comentario", command=self.add_comment)
        self.add_comment_button.pack(side=tk.LEFT)

    def update_users_list(self):
        self.users_listbox.delete(0, tk.END)
        for user in self.users.keys():
            if user != self.current_user:
                self.users_listbox.insert(tk.END, user)

    def add_post(self):
        post_text = self.new_post_entry.get()
        if post_text:
            self.users[self.current_user]['posts'].append(post_text)
            self.post_area.config(state=tk.NORMAL)
            self.post_area.insert(tk.END, f"{self.current_user}: {post_text}\n\n")
            self.post_area.config(state=tk.DISABLED)
            self.new_post_entry.delete(0, tk.END)

    def send_message(self):
        message_text = self.new_message_entry.get()
        if message_text:
            self.messages_area.config(state=tk.NORMAL)
            self.messages_area.insert(tk.END, f"{self.current_user}: {message_text}\n")
            self.messages_area.config(state=tk.DISABLED)
            self.new_message_entry.delete(0, tk.END)

    def add_friend(self):
        friend_name = self.add_friend_entry.get()
        if friend_name in self.users and friend_name != self.current_user:
            if friend_name not in self.users[self.current_user]['friends']:
                self.users[self.current_user]['friends'].append(friend_name)
                self.friends_listbox.insert(tk.END, friend_name)
                self.add_notification(f"¡{friend_name} ha sido agregado como amigo!")
                self.add_friend_entry.delete(0, tk.END)
            else:
                messagebox.showinfo("Información", "Ya eres amigo de este usuario.")
        else:
            messagebox.showerror("Error", "Usuario no encontrado o mismo usuario.")

    def add_comment(self):
        comment_text = self.new_comment_entry.get()
        if comment_text:
            self.comments_area.config(state=tk.NORMAL)
            self.comments_area.insert(tk.END, f"{self.current_user}: {comment_text}\n")
            self.comments_area.config(state=tk.DISABLED)
            self.new_comment_entry.delete(0, tk.END)

    def view_profile(self):
        user_profile = self.users.get(self.current_user, {})
        self.profile_text.config(
            text=f"Nombre: {self.current_user}\nBio: Aquí va la biografía del usuario.\n\nAmigos: {', '.join(user_profile.get('friends', []))}"
        )

    def add_notification(self, text):
        self.notifications_area.config(state=tk.NORMAL)
        self.notifications_area.insert(tk.END, f"Notificación: {text}\n")
        self.notifications_area.config(state=tk.DISABLED)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username in self.users and self.users[username]['password'] == password:
            self.current_user = username
            self.create_main_frame()
        else:
            messagebox.showerror("Error", "Nombre de usuario o contraseña incorrectos")

    def register(self):
        username = simpledialog.askstring("Registrar", "Ingrese un nombre de usuario:")
        if username and username not in self.users:
            password = simpledialog.askstring("Registrar", "Ingrese una contraseña:", show='*')
            if password:
                self.users[username] = {'password': password, 'friends': [], 'posts': []}
                messagebox.showinfo("Registro", "Usuario registrado con éxito")
                self.username_entry.delete(0, tk.END)
                self.password_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Nombre de usuario ya existe o inválido")

if __name__ == "__main__":
    root = tk.Tk()
    app = SocialNetworkApp(root)
    root.mainloop()
