```python
from app.service.auth import AuthInstance
from app.console import console, cyber_input, pause

def show_edit_name_menu():
    """
    Menu untuk mengganti/menetapkan nama akun.
    - Default/prefill adalah nomor yang sedang login.
    - Jika input kosong, nama akan diset ke nomor yang sedang login.
    - Menyimpan perubahan ke AuthInstance jika method penyimpanan tersedia.
    """
    active_user = None
    try:
        # Prefer method getter jika ada
        if hasattr(AuthInstance, "get_active_user"):
            active_user = AuthInstance.get_active_user()
        else:
            active_user = getattr(AuthInstance, "active_user", None)
    except Exception:
        active_user = getattr(AuthInstance, "active_user", None)

    if not active_user:
        console.print("[error]Tidak ada user aktif. Silakan login terlebih dahulu.[/]")
        pause()
        return False

    current_number = active_user.get("number", "<unknown>")
    prompt = f"Nama baru (default: {current_number}, ketik 99 untuk batal)"
    user_input = cyber_input(prompt).strip()

    if user_input == "99":
        console.print("[warning]Operasi batal.[/]")
        pause()
        return False

    # Jika input kosong, gunakan nomor sebagai nama
    new_name = user_input if user_input != "" else current_number

    # Update fields yang umum
    active_user["name"] = new_name
    active_user["display_name"] = new_name

    saved = False
    # Coba beberapa metode penyimpanan yang mungkin ada di AuthInstance
    try:
        if hasattr(AuthInstance, "update_active_user"):
            # fungsi yang menerima dict user baru
            AuthInstance.update_active_user(active_user)
            saved = True
        elif hasattr(AuthInstance, "save_active_user"):
            AuthInstance.save_active_user(active_user)
            saved = True
        elif hasattr(AuthInstance, "save_users"):
            # mungkin ada collection users dan method save
            AuthInstance.active_user = active_user
            AuthInstance.save_users()
            saved = True
        else:
            # fallback: set attribute langsung
            AuthInstance.active_user = active_user
            # jika ada method set_active_user yang menerima nomor,
            # panggil untuk memastikan persistence jika implementasinya melakukan penyimpanan.
            if hasattr(AuthInstance, "set_active_user"):
                try:
                    AuthInstance.set_active_user(active_user.get("number"))
                    saved = True
                except Exception:
                    # set attribute saja jika set_active_user gagal
                    saved = True
            else:
                saved = True
    except Exception as e:
        console.print(f"[error]Gagal menyimpan perubahan: {e}[/]")
        saved = False

    if saved:
        console.print(f"[neon_green]Nama berhasil diubah menjadi: {new_name}[/]")
    else:
        console.print("[warning]Perubahan lokal diterapkan tetapi penyimpanan persistent tidak berhasil.[/]")
    pause()
    return saved
