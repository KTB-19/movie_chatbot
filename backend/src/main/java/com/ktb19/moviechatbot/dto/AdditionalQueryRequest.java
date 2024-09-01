package com.ktb19.moviechatbot.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.Valid;
import jakarta.validation.constraints.Pattern;
import jakarta.validation.constraints.Size;
import lombok.Getter;
import lombok.Setter;

@Schema(description = "추가 질문 요청")
@Getter
@Setter
public class AdditionalQueryRequest {

    @Valid
    private ParsedQueryRequest parsedQuery;

    @Schema(description = "추가 질문", example = "대구 동성로에서 보려고")
    @Size(min = 1, max = 200)
    @Pattern(regexp = "^[가-힣ㄱ-ㅎㅏ-ㅣa-zA-Z0-9 !#$%&'*+/=?`{(|)}~^.-]*$", message = "한글, 영어, 숫자, 특수문자만 입력할 수 있습니다.")
    private String message;
}
