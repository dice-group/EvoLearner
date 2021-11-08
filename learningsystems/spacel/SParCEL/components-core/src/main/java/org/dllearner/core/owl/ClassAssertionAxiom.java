/**
 * Copyright (C) 2007-2011, Jens Lehmann
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

package org.dllearner.core.owl;

import java.util.Map;

/**
 * Represents a concept assertion in a knowledge base / ontology, 
 * e.g. "heiko is a person", "heiko is a male person having one child".
 * 
 * @author Jens Lehmann
 *
 */
public class ClassAssertionAxiom extends AssertionalAxiom {
	
	/**
	 * 
	 */
	private static final long serialVersionUID = -790952686329481774L;
	private Description concept;
	private Individual individual;
	
	public ClassAssertionAxiom(Description concept, Individual individual) {
		this.concept = concept;
		this.individual = individual;
	}

	public Description getConcept() {
		return concept;
	}

	public Individual getIndividual() {
		return individual;
	}

	public int getLength() {
		return 1 + concept.getLength();
	}
		
	public String toString(String baseURI, Map<String,String> prefixes) {
		return concept.toString(baseURI, prefixes) + "(" + individual.toString(baseURI, prefixes) + ")";
	}
	
	public String toKBSyntaxString(String baseURI, Map<String,String> prefixes) {
		return concept.toKBSyntaxString(baseURI, prefixes) + "(" + individual.toKBSyntaxString(baseURI, prefixes) + ")";
	}
	
	/*@Override
	public String toKBSyntaxString() {
		return concept.toKBSyntaxString() + "(" + individual + ")";
	}*/
	
	@Override
	public void accept(AxiomVisitor visitor) {
		visitor.visit(this);
	}	
	
	public void accept(KBElementVisitor visitor) {
		visitor.visit(this);
	}

	/* (non-Javadoc)
	 * @see org.dllearner.core.owl.KBElement#toManchesterSyntaxString(java.lang.String, java.util.Map)
	 */
	@Override
	public String toManchesterSyntaxString(String baseURI, Map<String, String> prefixes) {
		// TODO Auto-generated method stub
		return null;
	}	
}
