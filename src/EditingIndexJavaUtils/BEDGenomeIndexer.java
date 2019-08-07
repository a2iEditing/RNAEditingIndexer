/*
This work is licensed under the Creative Commons Attribution-Non-Commercial-ShareAlike 4.0 International License.
To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
For use of the software by commercial entities, please inquire with Tel Aviv University at ramot@ramot.org.
© 2019 Tel Aviv University (Erez Y. Levanon, Erez.Levanon@biu.ac.il;
Eli Eisenberg, elieis@post.tau.ac.il;
Shalom Hillel Roth, shalomhillel.roth@live.biu.ac.il).
*/

package EditingIndexJavaUtils;

import org.apache.commons.cli.*;

import java.io.*;
import java.util.HashMap;
import java.util.Map;
import java.util.Objects;
import java.util.TreeMap;

public class BEDGenomeIndexer {
    private static Map<String, Map<Integer, String>> GenerateIndex(String inputBED, String genomeFASTA,
                                                                   String bedtoolsPath) throws Exception {
        String line = null;
        String region, fastaSeq;
        int start;
        String[] recs;
        boolean fastaBEDNotEmpty = false;
        Map<String, Map<Integer, String>> indexedGenomeAtBEDRegions = new HashMap<>();
        StringBuilder bedtoolsCMD = new StringBuilder(bedtoolsPath).append(" getfasta -name -bedOut");
        bedtoolsCMD.append(String.format(" -fi '%s'", genomeFASTA));
        bedtoolsCMD.append(String.format(" -bed '%s'", inputBED));
        System.out.println("Running: ".concat(bedtoolsCMD.toString()));
        ProcessBuilder processBuilder = new ProcessBuilder("sh", "-c", bedtoolsCMD.toString());
        processBuilder.redirectErrorStream(true);
        Process p = processBuilder.start();
        BufferedReader r = new BufferedReader(new InputStreamReader(p.getInputStream()));

        System.out.println("GenerateIndex - Indexing FASTA Records!");
        while (true) {
            try {
                line = r.readLine();
                if (line == null || line.isEmpty()) {
                    if (fastaBEDNotEmpty) {
                        break;
                    } else {
                        System.out.println("GenerateIndex - getfasta Failed! Empty Output was Found");
                        System.exit(1);
                    }
                }
                if (line.contains("WARNING.")) {
                    continue;
                }

                recs = line.split(BEDUtilsConsts.BED_SEPARATOR);
                region = recs[BEDUtilsConsts.REGION_I];
                start = Integer.parseInt(recs[BEDUtilsConsts.START_I]);
                fastaSeq = recs[recs.length - BEDUtilsConsts.FASTA_SEQ_NEG_I];
                fastaBEDNotEmpty = true;
                if (!fastaSeq.matches("^[acgtnruksymwrbdhvACGTNRUKSYMWRBDHV\\-]+$")) {
                    System.out.println("GenerateIndex - Input BED is not of the Right Format!");
                    System.exit(1);
                }
                if (!indexedGenomeAtBEDRegions.containsKey(region)) {
                    Map<Integer, String> newI = new TreeMap<>();
                    indexedGenomeAtBEDRegions.put(region, (Map) newI);
                }
                indexedGenomeAtBEDRegions.get(region).put(start, fastaSeq);
            } catch (java.lang.ArrayIndexOutOfBoundsException e) {
                System.out.println("GenerateIndex - encountered unexpected line from bedtools, skipping line.\n Line:" + line);
            }
        }

        return indexedGenomeAtBEDRegions;
    }


    public static void main(String[] args) {
        Options options = new Options();
        Option input = new Option("i", "inputBED", true, "input BED file path");
        input.setRequired(true);
        options.addOption(input);

        Option output = new Option("o", "indexOutputPath", true, "Genome index output path");
        output.setRequired(true);
        options.addOption(output);


        Option genomeOption = new Option("g", "genomeFASTA", true, "The path to the genome.");
        genomeOption.setRequired(true);
        options.addOption(genomeOption);

        Option bedToolsOption = new Option("b", "bedtools", true, "The bedtools invoke cmd.");
        bedToolsOption.setRequired(false);
        options.addOption(bedToolsOption);

        CommandLineParser parser = new DefaultParser();
        HelpFormatter formatter = new HelpFormatter();
        CommandLine cmd = null;


        Map<String, Map<Integer, String>> genomeIndex = null;

        try {
            cmd = parser.parse(options, args);
        } catch (ParseException e) {
            System.out.println(e.getMessage());
            formatter.printHelp("GenerateIndex", options);
            System.exit(1);
        }

        String inputFilePath = cmd.getOptionValue(input.getOpt());
        String outputFilePath = cmd.getOptionValue(output.getOpt());
        String genomePath = cmd.getOptionValue(genomeOption.getOpt());
        String bedtools = cmd.getOptionValue(bedToolsOption.getOpt(), "bedtools");
        System.out.println("GenerateIndex - Starting!");
        try {
            genomeIndex = GenerateIndex(inputFilePath, genomePath, bedtools);
        } catch (Exception e) {
            System.out.println("GenerateIndex - Failed!");
            e.printStackTrace();
            System.exit(1);
        }

        try {
            FileOutputStream oStream = new FileOutputStream(outputFilePath);
            ObjectOutputStream obejctOutStream = new ObjectOutputStream(oStream);
            obejctOutStream.writeObject(genomeIndex);
        } catch (IOException e) {
            System.out.println("GenerateIndex - Cannot Create Index Output File");
            e.printStackTrace();
            System.exit(1);
        }
        System.out.println("GenerateIndex - Done Converting, Outputted to " + outputFilePath);

        System.exit(0);
    }

}
