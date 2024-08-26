package com.ktb19.moviechatbot.config;

import com.ktb19.moviechatbot.exception.common.ErrorResponse;
import io.swagger.v3.oas.models.Components;
import io.swagger.v3.oas.models.OpenAPI;
import io.swagger.v3.oas.models.info.Info;
import io.swagger.v3.oas.models.media.Content;
import io.swagger.v3.oas.models.media.MediaType;
import io.swagger.v3.oas.models.media.Schema;
import io.swagger.v3.oas.models.responses.ApiResponse;
import io.swagger.v3.oas.models.responses.ApiResponses;
import org.springdoc.core.customizers.OperationCustomizer;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import java.util.LinkedHashMap;
import java.util.Map;

@Configuration
public class SwaggerConfig {

    @Bean
    public OpenAPI customOpenAPI() {
        return new OpenAPI()
                .components(new Components())
                .info(new Info().title("무비빔밥")
                        .description("여러 영화관의 정보를 통합하여 제공하는 지능형 고객 지원 챗봇입니다.")
                        .version("1.0"));
    }

    /**
     * Operation 의 기존 ApiResponse 에 공통 응답 추가
     */
    @Bean
    public OperationCustomizer operationCustomizer() {
        return (operation, handlerMethod) -> {
            ApiResponses apiResponses = operation.getResponses();
            if (apiResponses == null) {
                apiResponses = new ApiResponses();
                operation.setResponses(apiResponses);
            }
            apiResponses.putAll(getCommonResponses());
            return operation;
        };
    }

    /**
     * 공통 응답 정보를 생성하여 맵으로 리턴한다.
     *
     * @return LinkedHashMap<String, ApiResponse> ApiResponse Map
     */
    private Map<String, ApiResponse> getCommonResponses() {
        LinkedHashMap<String, ApiResponse> responses = new LinkedHashMap<>();
        responses.put("400", badRequestResponse());
        responses.put("500", internalServerResponse());
        return responses;
    }

    /**
     * 400 Response 를 생성하여 리턴
     *
     * @return ApiResponse 400 응답 객체
     */
    private ApiResponse badRequestResponse() {
        ApiResponse apiResponse = new ApiResponse();
        apiResponse.setDescription("잘못된 입력 형식");
        addContent(apiResponse, "400", "Bad Request");
        return apiResponse;
    }

    /**
     * 500 Response 를 생성하여 리턴
     *
     * @return ApiResponse 500 응답 객체
     */
    private ApiResponse internalServerResponse() {
        ApiResponse apiResponse = new ApiResponse();
        apiResponse.setDescription("서버측 오류");
        addContent(apiResponse, "500", "Internal Server Error");
        return apiResponse;
    }

    /**
     * ApiResponse 의 Content 정보를 추가
     *
     * @param apiResponse Api 응답 객체
     * @param status      응답 상태 코드
     * @param message     응답 메시지
     */
    @SuppressWarnings("rawtypes")
    private void addContent(ApiResponse apiResponse, String status, String message) {
        Content content = new Content();
        MediaType mediaType = new MediaType();
        Schema schema = new Schema<>();
        schema.$ref("#/components/schemas/ErrorResponse");
        mediaType.schema(schema).example(new ErrorResponse(status, message));
        content.addMediaType("application/json", mediaType);
        apiResponse.setContent(content);
    }

}
