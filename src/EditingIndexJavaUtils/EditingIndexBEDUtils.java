package EditingIndexJavaUtils;

import java.util.Arrays;

public class EditingIndexBEDUtils {
    private final static String GENOME_INDEXER = "GenerateIndex";
    private final static String PILEUP_TO_COUNT = "PileupToCount";
    private final static String[] POSSIBLE_TOOLS = new String[] {GENOME_INDEXER, PILEUP_TO_COUNT};
    private final static StringBuilder USAGE = new StringBuilder().append("Please Call One Of The Implemented Utils -");

    public static void main(String[] args) {
        if (args.length < 1) {
            for (String possible: POSSIBLE_TOOLS) {
                USAGE.append(String.format(", %s", possible));
            }
            System.out.println(USAGE);
            System.exit(1);
        }
        switch (args[0]) {
            case GENOME_INDEXER:
                BEDGenomeIndexer.main(Arrays.copyOfRange(args, 1, args.length));
                break;
            case PILEUP_TO_COUNT:
                PileupToCount.main(Arrays.copyOfRange(args, 1, args.length));
                break;
            default:
                System.out.println(USAGE);
                System.exit(1);
        }
    }
}
