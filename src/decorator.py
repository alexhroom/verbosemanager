from . import VerboseManager


def verbosify(n_steps):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                verbose = kwargs['verbose']
            except KeyError:
                raise Exception("Function does not have the keyword argument 'verbose'")

            verbose_manager = VerboseManager.instance()
            verbose_manager.start(n_steps, verbose)
            func(*args, **kwargs)
            verbose_manager.finish(func.__name__.title())

        return wrapper
    return decorator
