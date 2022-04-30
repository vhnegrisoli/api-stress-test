import java.io.IOException;
import java.math.BigDecimal;
import java.math.RoundingMode;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.UUID;
import java.util.stream.IntStream;

public class StressTest {

    private static final Config CONFIG = new Config();
    private static final List<Integer> TIMER = new ArrayList<>();
    private static final List<String> REQUESTS_IDS = new ArrayList<>();
    private static final List<String> TOTAIS = new ArrayList<>();


    private static final String EMPTY = "";

    public static void main(String[] args) throws InterruptedException {
        defineTimeAndConcurrency(args);
        System.out.printf("Enviando %s usuários durante %s segundos...%n", CONFIG.getConcorrencia(), CONFIG.getTempo());
        new Thread(startTime).start();
        Thread.sleep(Constants.UM_SEGUNDO / 2);
        new Thread(displayMetrics).start();
        IntStream
            .range(Constants.ZERO, CONFIG.getConcorrencia())
            .forEach(usuario -> new Thread(createThread).start());
    }

    private static void defineTimeAndConcurrency(String[] args) {
        if (Utils.isEmpty(args) || args.length < 2) return;
        var concurrency = args[0];
        var time = args[1];
        if (!Utils.isEmpty(concurrency) && isNumericString(concurrency)) {
            CONFIG.setConcorrencia(Integer.parseInt(concurrency));
        }
        if (!Utils.isEmpty(time) && isNumericString(time)) {
            CONFIG.setTempo(Integer.parseInt(time));
        }
    }

    private static boolean isNumericString(String value) {
        try {
            Integer.parseInt(value);
            return true;
        } catch (Exception ex) {
            return false;
        }
    }

    private static final Runnable startTime = () -> {
        try {
            TIMER.add(1);
            IntStream
                    .range(Constants.ZERO, CONFIG.getTempo())
                    .forEach(i -> {
                        try {
                            Thread.sleep(Constants.UM_SEGUNDO);
                        } catch (Exception ex) {
                            ex.printStackTrace();
                        }
                    });
            TIMER.clear();
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    };

    private static final Runnable createThread = () -> {
        try {
            while (!Utils.isEmpty(TIMER)) {
                callHttpRequest();
            }
        } catch (Exception ex){
            ex.printStackTrace();
        }
    };

    private static final Runnable displayMetrics = () -> {
        try {
            while (!Utils.isEmpty(REQUESTS_IDS) || !Utils.isEmpty(TIMER)) {
                System.out.print(EMPTY);
            }
            var total = TOTAIS.size();
            var sucessos = TOTAIS.stream().filter(Constants.SUCCESS::equals).count();
            var falhas = TOTAIS.stream().filter(Constants.FAIL::equals).count();
            var disponibilidade = (sucessos / total) * 100;
            displayMetrics(total, sucessos, falhas, disponibilidade);
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    };

    private static void displayMetrics(int total,
                                       long sucessos,
                                       long falhas,
                                       long disponibilidade) {
        System.out.println("Total: " + total);
        System.out.println("Sucessos: " + sucessos);
        System.out.println("Falhas: " + falhas);
        System.out.println("Disponibilidade: " + disponibilidade + "%");
    }

    private static void callHttpRequest() {
        try {
            var uuid = UUID.randomUUID().toString();
            REQUESTS_IDS.add(uuid);
            var request = getRequestConfig();
            var startTime = System.currentTimeMillis();
            var response = createHttpResponse(request);
            var endTime = BigDecimal
                .valueOf(System.currentTimeMillis() - startTime)
                .setScale(Constants.ROUND_2_DECIMALS, RoundingMode.UP);
            var code = response.statusCode();
            printResponse(code, endTime);
            REQUESTS_IDS.remove(uuid);
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }

    private static void printResponse(int code, BigDecimal endTime) {
        if (isSuccessStatus(code)) {
            TOTAIS.add(Constants.SUCCESS);
            System.out.printf("%s - %s - Resposta: %s - %sms%n", Config.URL, Config.HTTP_METHOD, code, endTime);
        } else {
            TOTAIS.add(Constants.FAIL);
            System.out.printf("%s - %s - Resposta: %s - %sms - ERROR%n", Config.URL, Config.HTTP_METHOD, code, endTime);
        }
    }

    private static HttpResponse<String> createHttpResponse(HttpRequest request)
            throws IOException, InterruptedException {
        return HttpClient
                .newBuilder()
                .build()
                .send(request, HttpResponse.BodyHandlers.ofString());
    }

    private static HttpRequest getRequestConfig() {
        try {
            return HttpRequest
                .newBuilder()
                .method(Config.HTTP_METHOD, HttpRequest.BodyPublishers.noBody())
                .uri(new URI(Config.URL))
                .setHeader(Config.CONTENT_TYPE_HEADER_NAME, Config.APPLICATION_JSON)
                .build();
        } catch (Exception ex) {
            ex.printStackTrace();
            return null;
        }
    }

    private static boolean isSuccessStatus(int statusCode) {
        return statusCode >= Constants.SUCCESS_START && statusCode <= Constants.SUCCESS_END;
    }
}
