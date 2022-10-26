Módulo de Releases & Task Service Now SGT ONEFCC

==============================
Releases
De prueba: RLSE0595100
==============================
Módulo: sgt_onefcc_servicenow_release
Funciones:
    - Crear
    - Actualizar
    - Cancelar (TODO)
    - Aprobar (TODO)

    state:
        present, create, new
        to_certification
        approve
        to_preprod
        info_release
            - release
        





Parámetros
    state: present | absent | update | approve
    usuario:
    password:
    instancia_sn:
    
    create:
        - product *
        - group * 
        - reason *
        - risk *
        - short_description *
        - description *
        - justification *
        - implementation plan *
        - preprod_proposed_date
        - start_date *
        - end_date *

=============================
TASKS
=============================
Módulo: sgt_onefcc_servicenow_task
Funciones:

    sn_user *
    sn_pass *
    sn_base *
    sn_uri
    timeout
    
    state:
        - present, create, new
        - closed
        - inprogress
        - incomplete
        - skipped
        - info

        present, create, new:
            - release
            - start_date
            - end_date
            - short_description
            - description
            - state_resolve
            - type
            - group
            - order
            - application
            - technology
            - version

        closed:
            - task
            - status *
            - close_code *
            - close_notes *
            - work_notes
            - assigned_to
        
        inprogress:
            - task
            - status *
            - close_code *
            - close_notes *
            - work_notes
            - assigned_to

        skipped:
            - task
            - status *
            - close_code *
            - close_notes *
            - work_notes
        
        incomplete:
            - task
            - status *
            - close_code *
            - close_notes *
            - work_notes

        info_task:
            - task *
 

    
Parámetros
    state: present | absent | update | approve
    usuario:
    password:
    instancia_sn:
    
    State = Crear
        release:
        fecha_inicio:
        fecha_fin:
        descripcion_corta:
        descripcion:
        tipo:
        grupo:
        tecnologia:
        version:
        aplicacion:
        orden:

    State = Completo
    State = Incompleto
    State = Omitir
    State = Proceso

=


    data: (opcional, si se encuentra se anulan las demás opciones)

    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