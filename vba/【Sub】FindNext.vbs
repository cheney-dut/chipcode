' FindNext有个致命的Bug，那就是它只能用于Sub过程里面，不能用于Function过程里面。
' 参考：
' Excel VBA FindNext函数问题 http://blog.sina.com.cn/s/blog_6b8f217e0100uv0q.html
' VBS高亮显示插件：https://github.com/SublimeText/VBScript

Sub testFindNext()
    Dim lookup_vector As Range      ' 搜索的区域
    Dim result_vector As Range      ' 结果区域
    Dim lookup_value As String      ' 要查找的值

    Dim FirstAddress As String
    Dim LISTAGG As String           ' 返回结果
    Dim ch As String                ' 间隔符

    ch = ", "

    lookup_value = Sheet1.Range("A3").Value
    Set lookup_vector = Range("B1:B111")
    Set result_vector = Range("C1:C111")

    With lookup_vector
        Set matchcell = .Find(what:=lookup_value)

        If Not matchcell Is Nothing Then
            FirstAddress = matchcell.Address

            Do
                If LISTAGG <> "" Then
                    LISTAGG = LISTAGG + ch
                End If
                LISTAGG = LISTAGG + Cells(matchcell.row, result_vector.Column)

                Set matchcell = .FindNext(after:=matchcell)

            Loop Until (matchcell Is Nothing) Or (matchcell.Address = FirstAddress)
        End If
    End With
    MsgBox LISTAGG
End Sub