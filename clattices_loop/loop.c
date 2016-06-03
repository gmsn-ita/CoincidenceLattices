#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "loop.h"

void loop (double angle_start, double angle_end, double angle_step, int Nmax, double tolerance, double angle_tolerance)
{
	FILE *outputFile, *inputFile;
	//~ FILE *debugFile;
	
	double xA_1, yA_1, xA_2, yA_2;
	double xB_1, yB_1, xB_2, yB_2;
	
	/* Opens the temporary file to import the lattice parameters of the combination */
	inputFile = fopen ("lattices.tmp", "r");
	
	if (inputFile == NULL) {
		printf ("Couldn't find file lattices.tmp!\n");
		return;
	}
		
	fscanf (inputFile, "%lf %lf", &xA_1, &xA_2);
	fscanf (inputFile, "%lf %lf", &yA_1, &yA_2);
	fscanf (inputFile, "%lf %lf", &xB_1, &xB_2);
	fscanf (inputFile, "%lf %lf", &yB_1, &yB_2);
	
	fclose(inputFile);
	
	/* Loops through the angles and vectors in order to seek coincidences
	 * and prints the output file with the solutions for each angle
	 */
	 
	outputFile = fopen ("coincidences.tmp", "w");
		
	//~ debugFile = fopen ("debug.tmp", "w");
	
	int m1, m2, n1, n2;
	double angle, angleRad, angle_Am_MBn, cosAngle;
	double xAm, yAm, xMBn, yMBn;
	double norm, normA, normB;
	
	for (angle = angle_start; angle < angle_end + angle_step; angle = angle + angle_step) {
		angleRad = angle*PI/180;
		
		fprintf (outputFile, "%.2f\n", angle);
		
		for (m1 = -Nmax; m1 <= Nmax; m1++) {
			for (m2 = -Nmax; m2 <= Nmax; m2++) {
				for (n1 = -Nmax; n1 <= Nmax; n1++) {
					for (n2 = -Nmax; n2 < Nmax; n2++) {
						// |Am - MBn| < tolerance
						xAm = m1*xA_1 + m2*xA_2;
						xMBn = n1*(xB_1*cos(angleRad) + yB_1*sin(angleRad)) + n2*(xB_2*cos(angleRad) + yB_2*sin(angleRad));
						
						yAm = m1*yA_1 + m2*yA_2;
						yMBn = n1*(-xB_1*sin(angleRad) + yB_1*cos(angleRad)) + n2*(-xB_2*sin(angleRad) + yB_2*cos(angleRad));
						
						normA = sqrtf (pow(xAm, 2) + pow(yAm, 2));
						normB = sqrtf (pow(xMBn, 2) + pow(yMBn, 2));
						
						if (normA >= normB)
							norm = normB;
						else
							norm = normA;
						
						
						// Angle between the two vectors
						cosAngle = (xAm*xMBn + yAm*yMBn)/(normA*normB);
						
						// To prevent rounding errors, which lead to cos > 1
						if (cosAngle > 1.0)
							cosAngle = 1.0;
							
						angle_Am_MBn = 180*acos(cosAngle)/PI;
						
						//~ For debugging:
						
						//~ fprintf (debugFile, "%d %d %d %d\n", m1, m2, n1, n2);
						//~ fprintf (debugFile, "%lf %lf %lf %lf\n", xAm, xMBn, yAm, yMBn);
						//~ fprintf (debugFile, "normA: %lf\n", normA);
						//~ fprintf (debugFile, "normB: %lf\n", normB);
						//~ fprintf (debugFile, "angle: %lf\n", angle_Am_MBn);
						
						if (sqrtf (pow(xAm - xMBn, 2) + pow(yAm - yMBn, 2))/norm < tolerance && fabs(angle_Am_MBn) < angle_tolerance)
							fprintf (outputFile, "%d %d %d %d\n", m1, m2, n1, n2);
					}
				}
			}
		}
		
		fprintf (outputFile, "\n");
	}
	
	fclose (outputFile);	
	
	//~ fclose (debugFile);	
}
