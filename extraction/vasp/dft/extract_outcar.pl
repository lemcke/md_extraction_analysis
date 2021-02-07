#!/usr/bin/env perl

use strict;
use warnings;
use v5.16;
use Cwd qw( getcwd );
use File::Spec;	# for `splitpath`
# use Data::Dumper;

my $start_dir = getcwd;

do {
	# ---- Get input file. ---- #
	my $arg = shift // "./OUTCAR";

	my ( $vol, $dir, $file ) = File::Spec->splitpath($arg);
	$file = "OUTCAR" if $file eq "";
	$dir = "." if $dir eq "";

	say "path: $dir, file: $file";

	chdir $dir;

	
	# ---- Initialize data. ---- #
	my $converge = 0;
	my $num_atoms = 0;
	my $potential_energy = "nan";
	my @cell;
	my @pos;	# positions
	my @frc;	# forces
	
	
	# ---- Parse data from input file. ---- #
	open ( my $in, "<", $file ) || die "Cannot open $file: $!\n";

	while (<$in>) {
		my @fields = split " ";
		next if scalar @fields < 2;
		
		# potential energy
		if ($fields[0] eq "energy" && $fields[1] eq "without") {
			$potential_energy =	$fields[-1];
		}
	
		# simulation cell
		elsif ($fields[0] eq "direct" && $fields[1] eq "lattice") {
			for (my $i = 0; $i < 3; $i++) {
				$_ = <$in>;
				my @subfields = split " ";
				$cell[$i][0] = $subfields[0];
				$cell[$i][1] = $subfields[1];
				$cell[$i][2] = $subfields[2];
			}	
		}
		
		# atomic positions and forces
		elsif ($fields[0] eq "POSITION" && $fields[1] eq "TOTAL-FORCE") {
			$_ = <$in>;
			$_ = <$in>;
			$num_atoms = 0;
			while (! /--/) {
				my @subfields = split " ";
				$pos[$num_atoms][0] = $subfields[0];
				$pos[$num_atoms][1] = $subfields[1];
				$pos[$num_atoms][2] = $subfields[2];
				$frc[$num_atoms][0] = $subfields[3];
				$frc[$num_atoms][1] = $subfields[4];
				$frc[$num_atoms][2] = $subfields[5];
				$num_atoms += 1;
				$_ = <$in>;
			}
		}

		# convergence
		elsif ($fields[0] eq "reached" && $fields[1] eq "required") {
			$converge = 1;	
		}

	}

	write_value("potential_energy.txt", $potential_energy);
	write_value("converge.txt", $converge);
	write_m3_array("cell.txt", \@cell);
	write_m3_array("force.txt", \@frc);
	write_m3_array("position.txt", \@pos);

	chdir $start_dir;
} while @ARGV;

sub write_value {
	my $filename = $_[0];
	my $value = $_[1];
	open (my $filehandle, ">", $filename)
		|| die "Cannot open file $filename: $!\n";
	print $filehandle $value;
	close $filehandle;
}

sub write_m3_array {
	my $filename = $_[0];
	my $arr_ref = $_[1];

	open (my $filehandle, ">", $filename)
		|| die "Cannot open file $filename: $!\n";
	for (@$arr_ref) {
		printf $filehandle "% f\t% f\t% f\n", $_->[0], $_->[1], $_->[2];
	}
	close $filehandle;
}
