from functools import wraps
from django.http import HttpResponseForbidden
from modules.auths.models import Account, Role

def role_required(allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            # Verifica si el usuario está autenticado
            if not request.user.is_authenticated:
                return HttpResponseForbidden("No estás autenticado.")
            
            account = Account.getAccount(request.user)
            if account is None:
                return HttpResponseForbidden("No estás autenticado.")

            # Verifica si el rol del usuario está en la lista permitida
            is_admin = False
            try:
                _ = account.roles.get(name='admin')
                is_admin = True
            except Role.DoesNotExist:
                pass

            if not is_admin:
                is_allowed = False
                for allowed_role in allowed_roles:
                    if account.roles.filter(name=allowed_role):
                        is_allowed = True
                        break
                if not is_allowed:
                    return HttpResponseForbidden("No tienes el rol adecuado para acceder.")
                
            # Si pasa las validaciones, ejecuta la vista
            return view_func(request, *args, **kwargs)
        
        return _wrapped_view
    return decorator
