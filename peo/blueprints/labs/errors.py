from peo.models.lab import Lab

errors = {
    Lab.DoesNotExist: dict(
        message="A lab with that ID no longer exists.",
        status=404
    ),
    Lab.NameAlreadyInUse: dict(
        message="A lab with that name already exists.",
        status=400
    ),
}
