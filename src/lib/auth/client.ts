export const authClient = {
  // Registro de usuario
  async signUp(values: {
    firstName: string;
    lastName: string;
    email: string;
    password: string;
  }) {
    try {
      const res = await fetch('http://localhost:8000/api/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          first_name: values.firstName,
          last_name: values.lastName,
          username: values.email, // Se guarda como 'username' en la base de datos
          password: values.password,
        }),
      });

      if (!res.ok) {
        const data = await res.json();
        return { error: data.detail || 'Server error' };
      }

      return { error: null };
    } catch (err) {
      return { error: 'Network error' };
    }
  },

  // Login de usuario
  async signIn(values: {
    email: string;
    password: string;
  }) {
    try {
      const res = await fetch('http://localhost:8000/api/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email: values.email, // Aquí debe ser 'email' porque el backend espera eso
          password: values.password,
        }),
      });

      const data = await res.json();

      if (!res.ok) {
        return { error: data.detail || 'Credenciales inválidas' };
      }

      localStorage.setItem('token', data.access_token);

      return { error: null };
    } catch (err) {
      return { error: 'Network error' };
    }
  }
};
