#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "loop.h"

void loop (double angle_start, double angle_end, double angle_step, int Nmax, double tolerance)
{
	FILE* outputFile, *inputFile;
	
	double xA_1, yA_1, xA_2, yA_2;
	double xB_1, yB_1, xB_2, yB_2;
	
	/* Opens the temporary file to import the lattice parameters of the combination */
	inputFile = fopen ("lattices.tmp", "r");
	
	fscanf (inputFile, "%lf %lf", &xA_1, &xA_2);
	fscanf (inputFile, "%lf %lf", &yA_1, &yA_2);
	fscanf (inputFile, "%lf %lf", &xB_1, &xB_2);
	fscanf (inputFile, "%lf %lf", &yB_1, &yB_2);
	
	fclose(inputFile);
	
	/* Loops through the angles and vectors in order to seek coincidences
	 * and prints the output file with the solutions for each angle
	 */
	 
	outputFile = fopen ("coincidences.tmp", "w");
	
	int m1, m2, n1, n2;
	double angle, angleRad;
	double xAm, yAm, xMBn, yMBn;
	double norm, normA, normB;
	
	for (angle = angle_start; angle <= angle_end; angle += angle_step) {
		angleRad = angle*180/PI;
		
		fprintf (outputFile, "%.2f\n", angle);
		
		for (m1 = -Nmax; m1 < Nmax; m1++) {
			for (m2 = -Nmax; m2 < Nmax; m2++) {
				for (n1 = -Nmax; n1 < Nmax; n1++) {
					for (n2 = -Nmax; n2 < Nmax; n2++) {
						// |Am - MBn| < tolerance
						xAm = m1*xA_1 + m2*xA_2;
						xMBn = n1*(xB_1 * cos (angleRad) + yB_1 * sin (angleRad)) + n2*(xB_2 * cos (angleRad) + yB_2 * sin (angleRad));
						
						yAm = m1*yA_1 + m2*yA_2;
						yMBn = n1*(- xB_1 * sin (angleRad) + yB_1 * cos (angleRad)) + n2*(-yB_2 * sin (angleRad) + yB_2 * cos (angleRad));
						
						normA = sqrtf (pow(xAm, 2) + pow(yAm, 2));
						normB = sqrtf (pow(xMBn, 2) + pow(yMBn, 2));
						
						if (normA >= normB)
							norm = normB;
						else
							norm = normA;
						
						if ((abs(xAm - xMBn)/norm < tolerance) && (abs(yAm - yMBn)/norm < tolerance))
							fprintf (outputFile, "% 3d % 3d % 3d % 3d\n", m1, m2, n1, n2);
					}
				}
			}
		}
		
		fprintf (outputFile, "\n");
	}
	
	fclose (outputFile);	
}
