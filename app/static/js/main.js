/**
 * GESTTATION - Scripts del frontend
 * 
 * Este archivo lo fui construyendo poco a poco según necesitaba funcionalidades.
 * Algunas cosas las saqué de Stack Overflow y las adapté, otras las hice yo
 * después de mucho trial and error con JavaScript.
 */

document.addEventListener('DOMContentLoaded', function() {
    
    // Debug para saber que carga bien (me ayudó mucho durante el desarrollo)
    console.log('GESTTATION iniciado');
    
    // Cerrar alertas automáticamente después de unos segundos
    // Esto lo añadí porque era molesto tener que cerrarlas manualmente
    var alertas = document.querySelectorAll('.alert');
    alertas.forEach(function(alerta) {
        // No cierro las de warning porque suelen ser importantes
        if (!alerta.classList.contains('alert-warning')) {
            setTimeout(function() {
                try {
                    var bsAlert = new bootstrap.Alert(alerta);
                    bsAlert.close();
                } catch(e) {
                    // A veces falla si el usuario ya la cerró, no pasa nada
                }
            }, 4000);
        }
    });
    
    // Confirmación antes de borrar cosas
    // Me pasó una vez que borré una empresa sin querer y perdí todos los datos
    document.querySelectorAll('.btn-danger[type="submit"]').forEach(function(btn) {
        btn.addEventListener('click', function(e) {
            var mensaje = this.getAttribute('data-confirm');
            if (!mensaje) {
                mensaje = '¿Seguro que quieres eliminar esto? No se puede deshacer!';
            }
            if (!confirm(mensaje)) {
                e.preventDefault();
            }
        });
    });
    
    // Inicializar tooltips de Bootstrap
    // Copié esto de la documentación de Bootstrap 5
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(el) {
        return new bootstrap.Tooltip(el);
    });
    
    // Marcar el enlace activo en el menú
    // Esto me costó bastante hacerlo bien con las subrutas
    var path = window.location.pathname;
    document.querySelectorAll('.navbar-nav .nav-link').forEach(function(link) {
        var href = link.getAttribute('href');
        if (href === path) {
            link.classList.add('active');
        } else if (href !== '/' && path.indexOf(href) === 0) {
            // Para subrutas tipo /empresas/1/editar
            link.classList.add('active');
        }
    });
    
    // Validación de formularios con Bootstrap
    var forms = document.querySelectorAll('.needs-validation');
    forms.forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });
    
    // Validar archivos antes de subirlos
    // Limito a 16MB porque más grande no tiene sentido para CSVs
    document.querySelectorAll('input[type="file"]').forEach(function(input) {
        input.addEventListener('change', function(e) {
            var file = e.target.files[0];
            if (!file) return;
            
            var tamañoMB = file.size / 1024 / 1024;
            var extension = file.name.split('.').pop().toLowerCase();
            
            if (tamañoMB > 16) {
                alert('Archivo muy grande! Máximo 16 MB');
                e.target.value = '';
                return;
            }
            
            // Solo permito estos formatos para importar notas
            if (['csv', 'xlsx', 'xls'].indexOf(extension) === -1) {
                alert('Formato no válido. Solo CSV o Excel');
                e.target.value = '';
            }
        });
    });
    
    // Evitar números negativos en campos que no tienen sentido
    document.querySelectorAll('input[type="number"][min="0"]').forEach(function(input) {
        input.addEventListener('keydown', function(e) {
            if (e.key === '-') {
                e.preventDefault();
            }
        });
    });
    
    // Prevenir envío doble de formularios
    // Esto pasaba mucho cuando la conexión iba lenta
    document.querySelectorAll('form').forEach(function(form) {
        var submitted = false;
        form.addEventListener('submit', function(e) {
            if (submitted) {
                e.preventDefault();
                return;
            }
            submitted = true;
            
            var btn = form.querySelector('button[type="submit"]');
            if (btn) {
                btn.disabled = true;
                // Guardo el texto original por si hay que restaurarlo
                btn.setAttribute('data-texto', btn.innerHTML);
                btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Espera...';
            }
            
            // Por si acaso falla algo, rehabilito el botón
            setTimeout(function() {
                submitted = false;
                if (btn) {
                    btn.disabled = false;
                    btn.innerHTML = btn.getAttribute('data-texto') || 'Enviar';
                }
            }, 5000);
        });
    });
    
    // Buscador en tablas - muy útil cuando hay muchos estudiantes
    document.querySelectorAll('[data-table-search]').forEach(function(input) {
        var tableId = input.getAttribute('data-table-search');
        var tabla = document.querySelector(tableId);
        
        if (tabla) {
            input.addEventListener('keyup', function() {
                var busqueda = this.value.toLowerCase();
                var filas = tabla.querySelectorAll('tbody tr');
                
                filas.forEach(function(fila) {
                    var texto = fila.textContent.toLowerCase();
                    fila.style.display = texto.indexOf(busqueda) > -1 ? '' : 'none';
                });
            });
        }
    });
    
    // Contador de caracteres para campos de texto largo
    // Lo puse en las notas de empresa que tienen límite
    document.querySelectorAll('textarea[maxlength]').forEach(function(textarea) {
        var max = textarea.getAttribute('maxlength');
        var contador = document.createElement('small');
        contador.className = 'text-muted d-block text-end';
        textarea.parentNode.appendChild(contador);
        
        function actualizar() {
            var quedan = max - textarea.value.length;
            contador.textContent = quedan + ' caracteres';
        }
        
        textarea.addEventListener('input', actualizar);
        actualizar();
    });
});


// Funciones auxiliares que uso en varios sitios

function formatearFecha(fecha) {
    // Formato español dd/mm/yyyy
    return new Date(fecha).toLocaleDateString('es-ES');
}

function formatearEuros(cantidad) {
    // Esto me lo enseñó mi tutor, muy útil
    return new Intl.NumberFormat('es-ES', {
        style: 'currency',
        currency: 'EUR'
    }).format(cantidad);
}

// Validar email - regex básica que encontré online
function esEmailValido(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

// Exportar tabla a CSV - lo necesité para sacar listados
function exportarCSV(tablaId, nombreArchivo) {
    var tabla = document.querySelector(tablaId);
    if (!tabla) {
        alert('No encuentro la tabla');
        return;
    }
    
    var csv = [];
    var filas = tabla.querySelectorAll('tr');
    
    filas.forEach(function(fila) {
        var datos = [];
        fila.querySelectorAll('td, th').forEach(function(celda) {
            // Escapo las comillas para que no rompa el CSV
            var texto = celda.textContent.trim().replace(/"/g, '""');
            datos.push('"' + texto + '"');
        });
        csv.push(datos.join(','));
    });
    
    var contenido = csv.join('\n');
    var blob = new Blob([contenido], { type: 'text/csv' });
    var link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = nombreArchivo || 'datos.csv';
    link.click();
}
