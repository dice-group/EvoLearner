package org.dllearner.cli.ParCEL;

import org.apache.log4j.Level;
import org.dllearner.algorithms.ParCEL.ParCELPosNegLP;
import org.dllearner.core.*;
import org.dllearner.core.owl.Description;
import org.dllearner.core.owl.Individual;
import org.dllearner.learningproblems.EvaluatedDescriptionPosNeg;
import org.dllearner.parser.KBParser;
import org.dllearner.parser.ParseException;
import org.semanticweb.owlapi.model.OWLClassExpression;
import org.semanticweb.owlapi.model.OWLDataFactory;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import uk.ac.manchester.cs.owl.owlapi.OWLDataFactoryImpl;

import java.io.IOException;
import java.util.Set;

import com.google.common.collect.Sets;

/**
 * Evaluate a class expression on a PosNegLP
 */
@ComponentAnn(name = "Expression validator", version = 0, shortName = "")
public class ExpressionValidation extends CLI{

	private static Logger logger = LoggerFactory.getLogger(ExpressionValidation.class);

	private KnowledgeSource knowledgeSource;
	private AbstractReasonerComponent rs;
	private ParCELPosNegLP lp;
	private OWLDataFactory dataFactory = new OWLDataFactoryImpl();

	public Set<String> getCov() {
		return this.cov;
	}

	public void setCov(Set<String> cov) {
		this.cov = cov;
	}
	private Set<String> cov;

	@Override
	public void init() throws IOException {
		if (context == null) {
			super.init();

            knowledgeSource = context.getBean(KnowledgeSource.class);
			rs = context.getBean(AbstractReasonerComponent.class);
			lp = context.getBean(ParCELPosNegLP.class);		
		}
	}

	@Override
	public void run() {
    	/*try {
			org.apache.log4j.Logger.getLogger("org.dllearner").setLevel(Level.toLevel(logLevel.toUpperCase()));
		} catch (Exception e) {
			logger.warn("Error setting log level to " + logLevel);
		}*/
		lp = context.getBean(ParCELPosNegLP.class);		
		rs = lp.getReasoner();

        //expression = OWLAPIUtils.fromManchester(this.expression.toString(), rs, dataFactory, true);

		//Set<Individual> pos = lp.getPositiveExamples();
		//Set<Individual> neg = lp.getNegativeExamples();
		//Set<Individual> tp = rs.hasType(des, pos);
		//Set<Individual> fp = rs.hasType(des, neg);
		//Set<Individual> tn = Sets.difference(neg, fp);
		//Set<Individual> fn = Sets.difference(pos, tp);
		//System.out.println("#EVAL# tp: " + tp.size());
		//System.out.println("#EVAL# fp: " + fp.size());
		//System.out.println("#EVAL# tn: " + tn.size());
		//System.out.println("#EVAL# fn: " + fn.size());
		Set<Individual> pos = lp.getPositiveExamples();
		Set<Individual> neg = lp.getNegativeExamples();
		int tp = 0;
		int fp = 0;
		int tn = 0;
		int fn = 0;
		for(Individual p: pos) {
			if(cov.contains(p.getURI().toString())){
				tp++;
			} else {
				fn++;
			}
		}
		for(Individual p: neg) {
			if(cov.contains(p.getURI().toString())){
				fp++;
			} else {
				tn++;
			}
		}
		System.out.println("#EVAL# tp: " + tp);
		System.out.println("#EVAL# fp: " + fp);
		System.out.println("#EVAL# tn: " + tn);
		System.out.println("#EVAL# fn: " + fn);
}
}
