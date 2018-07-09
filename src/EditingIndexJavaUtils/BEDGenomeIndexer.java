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
        String line, region, fastaSeq;
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
            line = r.readLine();
            if (line == null || line.isEmpty()) {
                if (fastaBEDNotEmpty) {
                    break;
                } else {
                    System.out.println("GenerateIndex - getfasta Failed! Empty Output was Found");
                    System.exit(1);
                }
            }
            if(line.contains("WARNING.")){
                continue;
            }

            fastaBEDNotEmpty = true;
            recs = line.split(BEDUtilsConsts.BED_SEPARATOR);
            region = recs[BEDUtilsConsts.REGION_I];
            start = Integer.parseInt(recs[BEDUtilsConsts.START_I]);
            fastaSeq = recs[BEDUtilsConsts.FASTA_SEQ_I];
            if (!indexedGenomeAtBEDRegions.containsKey(region)) {
                indexedGenomeAtBEDRegions.put(region, new TreeMap<>());
            }
            indexedGenomeAtBEDRegions.get(region).put(start, fastaSeq);
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
