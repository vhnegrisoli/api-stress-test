import java.math.BigDecimal;
import java.math.RoundingMode;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.util.ArrayList;
import java.util.List;
import java.util.UUID;
import java.util.stream.IntStream;

public class StressTest {

    private static final Integer CONCORRENCIA = 3;
    private static final Integer TEMPO = 20;

    private static final Integer UM_SEGUNDO = 1000;
    private static final Integer ZERO = 0;
    private static final List<Integer> TIMER = new ArrayList<>();
    private static final List<String> REQUESTS_IDS = new ArrayList<>();
    private static final List<String> TOTAIS = new ArrayList<>();
    private static final Integer SUCCESS_START = 200;
    private static final Integer SUCCESS_END = 299;

    public static void main(String[] args) throws InterruptedException {
        new Thread(startTime).start();
        Thread.sleep(UM_SEGUNDO);
        IntStream
            .range(ZERO, CONCORRENCIA)
            .forEach(usuario -> new Thread(createThread).start());

        while (!REQUESTS_IDS.isEmpty() || !TIMER.isEmpty()) {
            System.out.print("");
        }

        var total = TOTAIS.size();
        var sucessos = TOTAIS.stream().filter("Success"::equals).count();
        var falhas = TOTAIS.stream().filter("Fail"::equals).count();
        var disponibilidade = (sucessos / total) * 100;

        System.out.println("Total: " + total);
        System.out.println("Sucessos: " + sucessos);
        System.out.println("Falhas: " + falhas);
        System.out.println("Disponibilidade: " + disponibilidade + "%");
    }

    private static Runnable startTime = () -> {
        try {
            TIMER.add(1);
            var contador = TEMPO;
            while (contador > ZERO) {
                Thread.sleep(UM_SEGUNDO);
                contador--;
            }
            TIMER.clear();
        } catch (Exception ex){
            ex.printStackTrace();
        }
    };

    private static Runnable createThread = () -> {
        try {
            while (!TIMER.isEmpty()) {
                callHttpRequest();
            }
        } catch (Exception ex){
            ex.printStackTrace();
        }
    };

    private static void callHttpRequest() {
        try {
            var uuid = UUID.randomUUID().toString();
            REQUESTS_IDS.add(uuid);
            var request = getRequestConfig();
            var startTime = System.currentTimeMillis();
            var response = HttpClient
                .newBuilder()
                .build()
                .send(request, HttpResponse.BodyHandlers.ofString());
            var endTime = BigDecimal
                .valueOf(System.currentTimeMillis() - startTime)
                .setScale(2, RoundingMode.UP);
            var code = response.statusCode();
            REQUESTS_IDS.remove(uuid);
            if (code >= SUCCESS_START && code <= SUCCESS_END) {
                TOTAIS.add("Success");
                System.out.printf("%s - %s - Resposta: %s - %sms%n",
                    "https://correcao-api.herokuapp.com/api/auth/token", "POST", code, endTime);
            } else {
                TOTAIS.add("Fail");
                System.out.printf("%s - %s - Resposta: %s - %sms - ERROR%n",
                    "https://correcao-api.herokuapp.com/api/auth/token", "POST", code, endTime);
            }
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }

    private static HttpRequest getRequestConfig() {
        try {
            return HttpRequest
                .newBuilder()
                .method("POST", HttpRequest.BodyPublishers.ofString("{\"usuario\":\"nataliacmsa@gmail.com\",\"senha\":\"odisseuosolerte\"}"))
                .uri(new URI("https://correcao-api.herokuapp.com/api/auth/token"))
                .setHeader("api-secret", "correcao-api-tataia-base64-producao")
                .setHeader("content-type", "application/json")
                .build();
        } catch (Exception ex) {
            ex.printStackTrace();
            return null;
        }
    }
}
