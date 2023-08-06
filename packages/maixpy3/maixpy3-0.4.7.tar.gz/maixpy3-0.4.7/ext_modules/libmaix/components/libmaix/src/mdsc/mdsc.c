#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <malloc.h>
#include "mdsc.h"
#include "libmaix_nn.h"

#define debug_line //printf("%s:%d %s %s %s \r\n", __FILE__, __LINE__, __FUNCTION__, __DATE__, __TIME__)
FILE *load_file(char *filename)
{
    FILE *fp;
    if (NULL == (fp = fopen(filename, "r")))
    {
        perror("fopen");
        return NULL;
    }
    return fp;
}

char *get_key(char *line)
{
    char *strline = (char *)malloc(sizeof(char) * 1024);
    memcpy(strline, line, 1024);
    char *key = (char *)malloc(sizeof(char) * 32);
    memset(key,0,32);
    char *start, *end, *key_head;
    start = strline;
    end = strchr(strline, '=');
    key_head = key;
    while (start != end)
    {
        if (*start == ' ')
        {
            start++;
        }
        else
        {
            *key = *start;
            start++;
            key++;
        }
    }
    key =  '\0';
    return key_head;
}

float *get_float_value(char *line)
{
    float *value = (float *)malloc(sizeof(float) * 10);
    float *value_head = value;
    char *start = strchr(line, '=') + 1;
    char *tmp = strchr(start, ',');
    while (*start != '\n')
    {
        char *single_value = (char *)malloc(sizeof(char) * 10);
        char *single_value_head = single_value;
        if (tmp != NULL)
        {

            for (; start != tmp; start++)
            {
                if (*start == ' ')
                    continue;
                *single_value = *start;
                single_value++;
            }
            start++;
            *value = atof(single_value_head);
            value++;
            free(single_value_head);
            tmp = strchr(start, ',');
        }
        else
        {

            while(*start != '\n')
            {
                if (*start == ' ')
                {
                    start++;
                    continue;
                }
                *single_value = *start;
                single_value++;
                start++;
            }
            *value = atof(single_value_head);
            value++;
            free(single_value_head);
        }
    }
    return value_head;
}

char *get_sting_value(char *line)
{

    char *strline = (char *)malloc(sizeof(char) * 1024);
    if(strline == NULL)
    {
        printf("malloc strine buffer is faild\n");
    }
    memcpy(strline, line, 1024);
    char *string_value = (char *)malloc(sizeof(char) * 32);
    if(string_value ==  NULL)
    {
        printf("malloc strlinr value buffer is faild\n");
    }
    memset(string_value , 0 ,32);
    char *string_value_head = string_value;
    char *start = strchr(strline, '=') + 1;
    while (*start != '\n'  )
    {
        if (*start == ' ')
        {
            start++;
            continue;
        }
        *string_value = *start;
        string_value++;
        start++;
    }
    string_value = '\0';
    return string_value_head;
}

void set_inputs_value(float **values, ini_info_t *ini_info) // float**指向二维数组
{
    int input_num = ini_info->input_num;
    for (int i = 0; i != ini_info->input_num; i++)
    {
        for (int j = 0; j != 3; j++)
        {
            ini_info->inputs_shape[i][j] = (int)values[i][j];
        }
        int h = (int)values[i][0];
        int w = (int)values[i][1];
        int c = (int)values[i][2];
        if (h != 1 && w != 1 && c == 3)
        {
            // mean
            ini_info->mean[i][0] = values[i][3];
            ini_info->mean[i][1] = values[i][4];
            ini_info->mean[i][2] = values[i][5];

            // norm,
            ini_info->norm[i][0] = values[i][6];
            ini_info->norm[i][1] = values[i][7];
            ini_info->norm[i][2] = values[i][8];
        }
        else if (h != 1 && w != 1 && c == 1)
        {
            // mean
            ini_info->mean[i][0] = values[i][3];
            ini_info->mean[i][1] = ini_info->mean[i][0];
            ini_info->mean[i][2] = ini_info->mean[i][0];

            // norm
            ini_info->norm[i][0] = values[i][4];
            ini_info->norm[i][1] = ini_info->norm[i][0];
            ini_info->norm[i][2] = ini_info->norm[i][0];
        }
        else if (h == 1 && w == 1 && c != 1)
        {
            // mean
            ini_info->mean[i][0] = values[i][3];
            ini_info->mean[i][1] = ini_info->mean[i][0];
            ini_info->mean[i][2] = ini_info->mean[i][0];

            // norm
            ini_info->norm[i][0] = values[i][4];
            ini_info->norm[i][1] = ini_info->norm[i][0];
            ini_info->norm[i][2] = ini_info->norm[i][0];
        }
    }
}

void set_outputs_value(float **values, ini_info_t *ini_info)
{
    for (int i = 0; i != ini_info->output_num; i++)
    {
        for (int j = 0; j != 3; j++)
        {
            ini_info->outputs_shape[i][j] = (int)values[i][j];
        }
    }
}

void set_inputs_scale(float *values, ini_info_t *ini_info)
{
    for (int i = 0; i != ini_info->input_num; i++)
    {
        ini_info->inputs_scale[i] = values[i];
    }
}

void set_outputs_scale(float *values, ini_info_t *ini_info)
{
    for (int i = 0; i != ini_info->output_num; i++)
    {
        ini_info->ouputs_scale[i] = values[i];
    }
}

int get_section(FILE *fp, char *title, ini_info_t *ini_info)
{
    int flag = 0;
    char string_title[64], string_lines[1024];
    sprintf(string_title, "[%s]", title);
    // input
    if (0 == strcmp(title, "inputs"))
    {

        int input_num = 0;
        char **inputs_name = (char **)malloc(sizeof(char *) * MAX_LEN);
        if(inputs_name == NULL)
        {
            printf("malloc inputs_name names  buffer  is faild\n");
        }
        char **inputs_name_head = inputs_name;
        float **value = (float **)malloc(sizeof(float *) * MAX_LEN);
        if(value == NULL)
        {
            printf("malloc input valuse  buffer  is faild\n");
        }
        float **value_head = value;

        while (!feof(fp))
        {
            fgets(string_lines, 1024, fp);
            if (0 == strncmp(string_title, string_lines, strlen(string_title)))
            {

                flag = 1;
                continue;
            }
            else if (flag == 1 && (NULL != strchr(string_lines, '=')))
            {
                *inputs_name = get_key(string_lines);
                *value = get_float_value(string_lines);
                inputs_name++;
                value++;
                input_num++;
            }
            else if (strspn(string_lines, "\t\n") == strlen(string_lines))
            {

                flag = 0;
                continue;
            }
        }
        ini_info->input_num = input_num;
        ini_info->inputs = inputs_name_head;

        set_inputs_value(value_head , ini_info);
        rewind(fp);
    }
    // output
    else if (0 == strcmp(title, "outputs"))
    {

        int output_num = 0;
        char **outputs_name = (char **)malloc(sizeof(char *) * MAX_LEN);
        if(outputs_name == NULL)
        {
            printf("malloc output names  buffer  is faild\n");
        }
        char **outputs_name_head = outputs_name;
        float **value = (float **)malloc(sizeof(float *) * MAX_LEN);
        if(value == NULL)
        {
            printf("malloc output valuse  buffer  is faild\n");
        }
        float **value_head = value;

        while (!feof(fp))
        {
            fgets(string_lines, 1024, fp);

            if (0 == strncmp(string_title, string_lines, strlen(string_title)))
            {

                flag = 1;
                continue;
            }
            else if (flag == 1 && (NULL != strchr(string_lines, '=')))
            {
                *outputs_name = get_key(string_lines);
                *value = get_float_value(string_lines);
                outputs_name++;
                value++;
                output_num++;
            }
            else if (strspn(string_lines, " \t\n") == strlen(string_lines))
            {
                flag = 0;
                continue;
            }
        }
        ini_info->output_num = output_num;
        ini_info->outpus = outputs_name_head;
        set_outputs_value(value_head , ini_info);
        rewind(fp);
    }
    // basic extra and decoder
    else if (0 == strcmp(title, "basic"))
    {

        while (!feof(fp))
        {
            fgets(string_lines, 1024, fp);

            if (0 == strncmp(string_title, string_lines, strlen(string_title)))
            {

                flag = 1;
                continue;
            }
            else if (flag == 1 && (NULL != strchr(string_lines, '=')))
            {
                char *key = get_key(string_lines);

                char *value = get_sting_value(string_lines);

                if (0 == strcmp(key, "type")) // input scale
                {
                    ini_info->model_type = value;
                    printf("type len:%d, type:%s\n",strlen(value), value);
                }
                if (0 == strcmp(key, "bin"))
                {
                    ini_info->bin_path = value;
                    printf("bin len :%d , bin:%s\n",strlen(value), value);
                }
                if (0 == strcmp(key, "param"))
                {

                    ini_info->param_path = value;
                    printf("param len:%d, param:%s\n",strlen(value),value);
                }
            }
            else if (strspn(string_lines, " \t\n") == strlen(string_lines))
            {

                flag = 0;
                continue;
            }
        }

        rewind(fp);
    }

    // sacle
    else if (0 == strcmp(title, "extra"))
    {

        while (!feof(fp))
        {
            fgets(string_lines, 1024, fp);
            if (0 == strncmp(string_title, string_lines, strlen(string_title)))
            {
                flag = 1;
                continue;
            }
            else if (flag == 1 && (NULL != strchr(string_lines, '=')))
            {
                char *key = get_key(string_lines);
                float *value = get_float_value(string_lines);
                debug_line;
                int count = 0;
                if ( 0 == strcmp( key ,  "inputs_scale"))  // input scale
                {
                    debug_line;
                    for(int i = 0 ; i != ini_info->input_num ; i++)
                    {
                        ini_info->inputs_scale[i]  =value[i];
                    }
                }
                else
                {
                    debug_line;
                    for(int j = 0 ; j != ini_info->output_num ; j++)
                    {
                        ini_info->ouputs_scale[j] = value[j];
                    }
                }
            }
            else if (strspn(string_lines, " \t\n") == strlen(string_lines))
            {
                flag = 0;
                continue;
            }
        }
        rewind(fp);
    }
}

ini_info_t read_file (char * mdsc_path)
{
    FILE *fp = load_file(mdsc_path);
    if(fp == NULL)
    {
        printf("open %s is faild\n",mdsc_path);
    }
    ini_info_t ini_info;
    get_section(fp , "basic", &ini_info);
    get_section(fp, "inputs", &ini_info);
    get_section(fp , "outputs", &ini_info);
    get_section(fp , "extra", &ini_info);
    return ini_info;
}

// int main(int argc, char const *argv[])
// {
//     int i = 0;
//     if (argc == 1)
//     {
//         printf("there is not ini file path to read\n'");
//         return -1;
//     }

//     char *file_path = argv[1];
//     // get information from ini file
//     FILE *fp = load_file(file_path);
//     // set a object to save  information
//     ini_info_t ini_info;
//     // section basic
//     get_section(fp , "basic", &ini_info);
//     get_section(fp, "inputs", &ini_info);
//     get_section(fp , "outputs", &ini_info);
//     debug_line;
//     get_section(fp , "extra", &ini_info);
//     printf("____________________\n");
//     printf("type :%s \n", ini_info.model_type);
//     printf("bin:%s\n", ini_info.bin_path);
//     printf("param:%s\n", ini_info.param_path);
//     printf("input num:%d\n", ini_info.input_num);
//     for(int i =0 ; i != ini_info.input_num;i++)
//     {
//         printf("this is innput%d \n ",i+1);
//         // printf("name:%s\n",ini_info.inputs[i]);
//         printf("C:%d   H:%d   W:%d\n",ini_info.inputs_shape[i][0] , ini_info.inputs_shape[i][1] , ini_info.inputs_shape[i][2]);
//         printf("norm_R: %f ,norm_G : %f  ,norm_B :%f\n",ini_info.norm[i][0],ini_info.norm[i][1],ini_info.norm[i][2]);
//         printf("mean_R: %f ,mean_G : %f  ,mean_B :%f\n",ini_info.mean[i][0],ini_info.mean[i][1],ini_info.mean[i][2]);
//         printf("input scale :%f \n",ini_info.inputs_scale[i] );

//     }
//     printf("____________________\n");
//     for(int i=0 ; i != ini_info.output_num ;i++)
//     {
//         printf("this is output%d \n ",i+1);
//         // printf("'name : %s \n", ini_info.outpus[i]);
//         printf("C:%d   H:%d   W:%d\n",ini_info.outputs_shape[i][0] , ini_info.outputs_shape[i][1] , ini_info.outputs_shape[i][2]);
//         printf("output scale :%f \n",ini_info.ouputs_scale[i]);
//     }
//     printf("____________________\n");

// }

libmaix_nn_t* load_mdsc(char * path , ini_info_t * info_ptr)
{
    FILE *fp = load_file(path);
    if(fp == NULL)
    {
        printf("open %s is faild\n",path);
    }
    get_section(fp , "basic",info_ptr);
    get_section(fp, "inputs", info_ptr);
    get_section(fp , "outputs", info_ptr);
    get_section(fp , "extra", info_ptr);

    int res_h = info_ptr->inputs_shape[0][0];
    int res_w = info_ptr->inputs_shape[0][1];
    int res_c = info_ptr->inputs_shape[0][2];
    int input_w = res_w, input_h = res_h ,input_c = res_c;
    printf("input_w :%d   , input_h :%d \n",input_w , input_h);
    printf("- -init\n");
    libmaix_nn_model_path_t model_path;
    libmaix_nn_opt_param_t opt_param;
    libmaix_nn_t* nn = NULL;
    libmaix_err_t err =LIBMAIX_ERR_NONE;

    if(strcmp(info_ptr->model_type , "aipu") == 0)
    {
        printf("r329\n");
        if(strlen(info_ptr->bin_path) == 0)
        {
            printf("this path is empty ! \n");
        }
        //path
        model_path.aipu.model_path = info_ptr->bin_path;
        // opt
        opt_param.aipu.input_names = info_ptr->inputs;
        opt_param.aipu.output_names = info_ptr->outpus;
        opt_param.aipu.input_num = info_ptr->input_num;
        opt_param.aipu.output_num = info_ptr->output_num;
        for(int i=0 ; i !=3 ; i++ )
        {
            opt_param.aipu.mean[i] = info_ptr->mean[0][i];
            opt_param.aipu.norm[i] = info_ptr->norm[0][i];
        }
        for (int i =0 ; i != info_ptr->output_num ; i++)
        {
            opt_param.aipu.scale[i] = info_ptr->ouputs_scale[i];
        }

    }
    else if (strcmp(info_ptr->model_type , "awnn") == 0)
    {
        printf("v831\n");
        if(strlen(info_ptr->bin_path) == 0  ||  strlen(info_ptr->param_path)==0)
        {
            printf("this path is empty ! \n");

        }
        //path
        model_path.awnn.bin_path = info_ptr->bin_path;
        model_path.awnn.param_path = info_ptr->param_path;
        printf("bin: %s\nparam:%s \n",info_ptr->bin_path , info_ptr->param_path);
        //opt
        opt_param.awnn.input_names = info_ptr->inputs;
        opt_param.awnn.output_names = info_ptr->outpus;
        opt_param.awnn.input_num = info_ptr->input_num;
        opt_param.awnn.output_num = info_ptr->output_num;
        opt_param.awnn.encrypt = false;
        for(int i=0 ; i !=3 ; i++ )
        {
            opt_param.awnn.mean[i] = info_ptr->mean[0][i];
            opt_param.awnn.norm[i] = info_ptr->norm[0][i];
        }
        for (int i =0 ; i != 3 ; i++)
        {
            printf("mean%d : %f \n", i , opt_param.aipu.mean[i]);
            printf("norm%d : %f \n", i , opt_param.aipu.norm[i]);
        }
    }
    else
    {
        printf("this type value is empty or the type is unsupport !\n");
    }

    // nn create
    nn = libmaix_nn_create();
    if(!nn)
    {
        printf("libmaix_nn object create fail\n");
    }
    err = nn->init(nn);
    if(err != LIBMAIX_ERR_NONE)
    {
        printf("libmaix_nn init fail: %s\n", libmaix_get_err_msg(err));
    }
    printf("-- nn object load model\n");
    err = nn->load(nn, &model_path, &opt_param);
    printf("-- nn object load model is done");
    if(err != LIBMAIX_ERR_NONE)
    {
        printf("libmaix_nn load fail: %s\n", libmaix_get_err_msg(err));
    }
    return nn;
}


libmaix_nn_t* build_model(ini_info_t * info_ptr)
{
libmaix_nn_model_path_t model_path;
    libmaix_nn_opt_param_t opt_param;
    libmaix_nn_t* nn = NULL;
    libmaix_err_t err =LIBMAIX_ERR_NONE;

    if(strcmp(info_ptr->model_type , "aipu") == 0)
    {
        printf("r329\n");
        if(strlen(info_ptr->bin_path) == 0)
        {
            printf("this path is empty ! \n");
        }
        //path
        model_path.aipu.model_path = info_ptr->bin_path;
        // opt
        opt_param.aipu.input_names = info_ptr->inputs;
        opt_param.aipu.output_names = info_ptr->outpus;
        opt_param.aipu.input_num = info_ptr->input_num;
        opt_param.aipu.output_num = info_ptr->output_num;
        for(int i=0 ; i !=3 ; i++ )
        {
            opt_param.aipu.mean[i] = info_ptr->mean[0][i];
            opt_param.aipu.norm[i] = info_ptr->norm[0][i];
        }
        for (int i =0 ; i != info_ptr->output_num ; i++)
        {
            opt_param.aipu.scale[i] = info_ptr->ouputs_scale[i];
        }

    }
    else if (strcmp(info_ptr->model_type , "awnn") == 0)
    {
        printf("v831\n");
        if(strlen(info_ptr->bin_path) == 0  ||  strlen(info_ptr->param_path)==0)
        {
            printf("this path is empty ! \n");

        }
        //path
        model_path.awnn.bin_path = info_ptr->bin_path;
        model_path.awnn.param_path = info_ptr->param_path;
        printf("bin: %s\nparam:%s \n",info_ptr->bin_path , info_ptr->param_path);
        //opt
        opt_param.awnn.input_names = info_ptr->inputs;
        opt_param.awnn.output_names = info_ptr->outpus;
        opt_param.awnn.input_num = info_ptr->input_num;
        opt_param.awnn.output_num = info_ptr->output_num;
        opt_param.awnn.encrypt = false;
        for(int i=0 ; i !=3 ; i++ )
        {
            opt_param.awnn.mean[i] = info_ptr->mean[0][i];
            opt_param.awnn.norm[i] = info_ptr->norm[0][i];
        }
        for (int i =0 ; i != 3 ; i++)
        {
            printf("mean%d : %f \n", i , opt_param.aipu.mean[i]);
            printf("norm%d : %f \n", i , opt_param.aipu.norm[i]);
        }
    }
    else
    {
        printf("this type value is empty or the type is unsupport !\n");
    }

    // nn create
    nn = libmaix_nn_create();
    if(!nn)
    {
        printf("libmaix_nn object create fail\n");
    }
    err = nn->init(nn);
    if(err != LIBMAIX_ERR_NONE)
    {
        printf("libmaix_nn init fail: %s\n", libmaix_get_err_msg(err));
    }
    printf("-- nn object load model\n");
    err = nn->load(nn, &model_path, &opt_param);
    printf("-- nn object load model is done");
    if(err != LIBMAIX_ERR_NONE)
    {
        printf("libmaix_nn load fail: %s\n", libmaix_get_err_msg(err));
    }
    return nn;
}