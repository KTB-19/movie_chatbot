package com.ktb19.moviechatbot.config;

import io.swagger.v3.oas.models.Components;
import io.swagger.v3.oas.models.OpenAPI;
import io.swagger.v3.oas.models.info.Info;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

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
}
