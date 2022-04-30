public class Config {

    private Integer concorrencia = 10;
    private Integer tempo = 30;

    public static final String URL = "http://localhost:8080/api/v1/cep/86050523";
    public static final String HTTP_METHOD = "GET";
    public static final String CONTENT_TYPE_HEADER_NAME = "content-type";
    public static final String APPLICATION_JSON = "application/json";

    public Integer getConcorrencia() {
        return concorrencia;
    }

    public void setConcorrencia(Integer concorrencia) {
        this.concorrencia = concorrencia;
    }

    public Integer getTempo() {
        return tempo;
    }

    public void setTempo(Integer tempo) {
        this.tempo = tempo;
    }
}
