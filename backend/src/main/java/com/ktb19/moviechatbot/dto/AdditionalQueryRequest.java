package com.ktb19.moviechatbot.dto;

import com.ktb19.moviechatbot.constant.Constants;
import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.Valid;
import jakarta.validation.constraints.Pattern;
import jakarta.validation.constraints.Size;
import lombok.Getter;
import lombok.Setter;

import static com.ktb19.moviechatbot.constant.Constants.*;

@Schema(description = "추가 질문 요청")
@Getter
@Setter
public class AdditionalQueryRequest {

    @Valid
    private ParsedQueryRequest parsedQuery;

    @Schema(description = "추가 질문", example = "대구 동성로에서 보려고")
    @Size(min = 1, max = 200)
    @Pattern(regexp = PATTERN_REGEXP_ALL, message = PATTERN_REGEXP_ALL_MESSAGE)
    private String message;
}
