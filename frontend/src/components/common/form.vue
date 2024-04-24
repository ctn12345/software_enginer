<template>
     <!-- 新增参数弹窗 -->
    <el-dialog :close-on-click-modal="false" title="新增参数" :visible.sync="paramsVisible">
        <el-form :model="paramsForm">
            <el-form-item label="参数名称" label-width="120px">
                <el-input v-model="paramsForm.paramsName" autocomplete="off"></el-input>
            </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
            <el-button @click="cancelParams">取 消</el-button>
            <el-button type="primary" @click="addParams">确 定</el-button>
        </div>
    </el-dialog>
  </template>
  
  <script>
    export default{
        name:"form_flight"
    }
  
  </script>
  