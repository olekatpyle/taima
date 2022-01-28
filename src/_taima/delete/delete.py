from _taima.delete.queries import *

#-----------------------------------------------------------------------------
# Modulue to perform delete transactions on the database


# function for the argument handler, to run when argument 'wipe' was specified
def delete(args: tuple) -> None:
       
    args.pop('func')
    args.pop('subparser')
    
    passed_arg: str = None
    rows_affected: int = 0

    # find the flag that was passed as argument
    for arg in args:
        if args[arg] is None or args[arg] is False:
            pass
        else:
            passed_arg = arg
    
    if passed_arg == 'all':
        rows_affected = WIPE_DATABASE()
    
    elif passed_arg == 'task':
        task = args[passed_arg]
        rows_affected = DELETE_TASK(task)

    print(f'{rows_affected} ROW(S) affected..')
        
    exit()
