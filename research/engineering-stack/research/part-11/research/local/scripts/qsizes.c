#include <stdio.h>
#include <stdint.h>
#define GGML_COMMON_DECL_C
#include "ggml-common.h"
#define P(name, T, N) printf("%-8s block=%3d weights, %3zu bytes, %.4f bits/weight\n", name, (int)(N), sizeof(T), 8.0*sizeof(T)/(double)(N))
int main(void){
  P("q1_0",block_q1_0,QK1_0); P("q2_0",block_q2_0,QK2_0);
  P("q4_0",block_q4_0,QK4_0); P("q4_1",block_q4_1,QK4_1);
  P("q5_0",block_q5_0,QK5_0); P("q5_1",block_q5_1,QK5_1);
  P("q8_0",block_q8_0,QK8_0);
  P("mxfp4",block_mxfp4,QK_MXFP4); P("nvfp4",block_nvfp4,QK_NVFP4);
  P("q2_K",block_q2_K,QK_K); P("q3_K",block_q3_K,QK_K); P("q4_K",block_q4_K,QK_K);
  P("q5_K",block_q5_K,QK_K); P("q6_K",block_q6_K,QK_K);
  P("tq1_0",block_tq1_0,QK_K); P("tq2_0",block_tq2_0,QK_K);
  P("iq1_s",block_iq1_s,QK_K); P("iq1_m",block_iq1_m,QK_K);
  P("iq2_xxs",block_iq2_xxs,QK_K); P("iq2_xs",block_iq2_xs,QK_K); P("iq2_s",block_iq2_s,QK_K);
  P("iq3_xxs",block_iq3_xxs,QK_K); P("iq3_s",block_iq3_s,QK_K);
  P("iq4_nl",block_iq4_nl,QK4_NL); P("iq4_xs",block_iq4_xs,QK_K);
  return 0;
}
