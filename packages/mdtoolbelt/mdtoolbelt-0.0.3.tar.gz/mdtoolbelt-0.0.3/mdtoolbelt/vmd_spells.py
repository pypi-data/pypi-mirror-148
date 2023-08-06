# Functions powered by VMD
# Humphrey, W., Dalke, A. and Schulten, K., "VMD - Visual Molecular Dynamics", J. Molec. Graphics, 1996, vol. 14, pp. 33-38. 
# http://www.ks.uiuc.edu/Research/vmd/

import os

from subprocess import run, PIPE, STDOUT, Popen
from typing import Optional, List

from .single_frame_getter import get_last_frame
from .formats import get_format

# Set the script filename with all commands to be passed to vmd
commands_filename = '.commands.vmd'

# List all the vmd supported trajectory formats
vmd_supported_structure_formats = {'pdb', 'prmtop', 'psf', 'gro'} # DANI: Esto lo he hecho rápido, hay muchas más
vmd_supported_trajectory_formats = {'mdcrd', 'crd', 'dcd', 'xtc', 'trr', 'nc'}

# Given a vmd supported topology with no coordinates and a single frame file, generate a pdb file
def vmd_to_pdb (
    input_structure_filename : str,
    input_trajectory_filename : str,
    output_structure_filename : str):

    # DANI: Esto alomejor se podria substituit por un 'animate read' en los commands
    # https://www.ks.uiuc.edu/Research/vmd/current/ug/node121.html
    single_frame_filename = get_last_frame(input_structure_filename, input_trajectory_filename, vmd_supported_trajectory_formats)

    # Prepare a script for VMD to run. This is Tcl language
    with open(commands_filename, "w") as file:
        # Select all atoms
        file.write('set all [atomselect top "all"]\n')
        # Write the current topology in 'pdb' format
        file.write('$all frame first\n')
        file.write('$all writepdb ' + output_structure_filename + '\n')
        file.write('exit\n')

    # Run VMD
    logs = run([
        "vmd",
        input_structure_filename,
        single_frame_filename,
        "-e",
        commands_filename,
        "-dispdev",
        "none"
    ], stdout=PIPE).stdout.decode()

    os.remove(commands_filename)
# Set function supported formats
vmd_to_pdb.format_sets = [
    {
        'inputs': {
            'input_structure_filename': {'psf', 'parm', 'prmtop'},
            'input_trajectory_filename': vmd_supported_trajectory_formats
        },
        'outputs': {
            'output_structure_filename': {'pdb'}
        }
    }
]

# This tool allows you to set the chain of all atoms in a selection
# This is powered by VMD and thus the selection lenguage must be the VMD's
# Arguments are as follows:
# 1 - Input pdb filename
# 2 - Atom selection (All atoms by defualt)
# 3 - Chain letter (May be the flag 'fragment', which is the default indeed)
# 4 - Output pdb filename (Input filename by default)
# WARNING: When no selection is passed, if only a part of a "fragment" is missing the chain then the whole fragment will be affected
# WARNING: VMD only handles fragments if there are less fragments than letters in the alphabet
def chainer (
    input_pdb_filename : str,
    atom_selection : Optional[str] = None,
    chain_letter : Optional[str] = None,
    output_pdb_filename : Optional[str] = None
):

    # If no atom selection is provided then all atoms are selected
    if not atom_selection:
        atom_selection = 'all'

    # If no chain letter is provided then the flag 'fragment' is used
    if not chain_letter:
        chain_letter = 'fragment'

    # If no output filename is provided then use input filename as output filename
    if not output_pdb_filename:
        output_pdb_filename = input_pdb_filename

    # Check the file exists
    if not os.path.exists(input_pdb_filename):
        raise SystemExit('ERROR: The file does not exist')
       
    with open(commands_filename, "w") as file:
        # Select the specified atoms and set the specified chain
        file.write('set atoms [atomselect top "' + atom_selection + '"]\n')
        # In case chain letter is not a letter but the 'fragment' flag, asign chains by fragment
        # Fragments are atom groups which are not connected by any bond
        if chain_letter == 'fragment':
            # Get all different chain names
            file.write('set chains_sample [lsort -unique [${atoms} get chain]]\n')
            # Set letters in alphabetic order
            file.write('set letters "A B C D E F G H I J K L M N O P Q R S T U V W X Y Z"\n')
            # Get the number of fragments
            file.write('set fragment_number [llength [lsort -unique -integer [${atoms} get fragment]]]\n')
            # For each fragment, set the chain of all atoms which belong to this fragment alphabetically
            # e.g. fragment 0 -> chain A, fragment 1 -> chain B, ...
            file.write('for {set i 0} {$i <= $fragment_number} {incr i} {\n')
            file.write('	set fragment_atoms [atomselect top "fragment $i"]\n')
            file.write('	$fragment_atoms set chain [lindex $letters $i]\n')
            file.write('}\n')
            # Otherwise, set the specified chain
        else:
            file.write('$atoms set chain ' + chain_letter + '\n')
        # Write the current topology in 'pdb' format
        file.write('set all [atomselect top "all"]\n')
        file.write('$all frame first\n')
        file.write('$all writepdb ' + output_pdb_filename + '\n')
        file.write('exit\n')

    # Run VMD
    logs = run([
        "vmd",
        input_pdb_filename,
        "-e",
        commands_filename,
        "-dispdev",
        "none"
    ], stdout=PIPE).stdout.decode()

    # Remove the vmd commands file
    os.remove(commands_filename)

# Get vmd supported trajectories merged and converted to a different format
# WARNING: Note that this process is not memory efficient so beware the size of trajectories to be converted
# WARNING: The input structure filename may be None
def merge_and_convert_trajectories (
    input_structure_filename : Optional[str],
    input_trajectory_filenames : List[str],
    output_trajectory_filename : str
    ):

    # Get the format to export coordinates
    output_trajectory_format = get_format(output_trajectory_filename)

    # Although 'crd' and 'mdcrd' may be the same, VMD only recognizes 'crd' as exporting coordinates file type
    if output_trajectory_format == 'mdcrd':
        output_trajectory_format = 'crd'

    # Prepare a script for the VMD to automate the data parsing. This is Tcl lenguage
    # In addition, if chains are missing, this script asigns chains by fragment
    # Fragments are atom groups which are not connected by any bond
    with open(commands_filename, "w") as file:
        # Select all atoms
        file.write('set all [atomselect top "all"]\n')
        # Write the current trajectory in the specified format format
        file.write('animate write ' + output_trajectory_format + ' ' + output_trajectory_filename + ' waitfor all sel $all\n')
        file.write('exit\n')

    inputs = [ input_structure_filename, *input_trajectory_filenames ] if input_structure_filename else input_trajectory_filenames

    # Run VMD
    logs = run([
        "vmd",
        *inputs,
        "-e",
        commands_filename,
        "-dispdev",
        "none"
    ], stdout=PIPE, stderr=STDOUT).stdout.decode() # Redirect errors to the output in order to dont show them in console

    if not os.path.exists(output_trajectory_filename):
        print(logs)
        raise SystemExit('Something went wrong with VMD')

    # Remove the vmd commands file
    os.remove(commands_filename)

# Set function supported formats
merge_and_convert_trajectories.format_sets = [
    {
        'inputs': {
            'input_structure_filename': None,
            'input_trajectory_filenames': {'dcd', 'xtc', 'trr', 'nc'}
        },
        'outputs': {
            # NEVER FORGET: VMD cannot write to all formats it supports to read
            'output_trajectory_filename': {'mdcrd', 'crd', 'dcd', 'trr'}
        }
    },
    {
        'inputs': {
            'input_structure_filename': vmd_supported_structure_formats,
            'input_trajectory_filenames': {'mdcrd', 'crd'}
        },
        'outputs': {
            # NEVER FORGET: VMD cannot write to all formats it supports to read
            'output_trajectory_filename': {'mdcrd', 'crd', 'dcd', 'trr'}
        }
    }
]