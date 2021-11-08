/**
 * Copyright (C) 2007 - 2016, Jens Lehmann
 *
 * This file is part of DL-Learner.
 *
 * DL-Learner is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3 of the License, or
 * (at your option) any later version.
 *
 * DL-Learner is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */
package org.aksw.mlbenchmark.validation.measures;

/**
 * Accuracy calculation with true/false positive/negative
 */
public interface MeasureMethodTwoValued {
	/**
	 * Compute accuracy according to this method
	 * @param tp True Positives (positive as positive)
	 * @param fn False Negative (positive as negative)
	 * @param fp False Positive (negative as positive)
	 * @param tn True Negative (negative as negative)
	 * @return accuracy value
	 */
	double getMeasure(int tp, int fn, int fp, int tn);
}
